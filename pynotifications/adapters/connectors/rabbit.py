from typing import Callable, Dict
import pynotifications.connector
import json
import pika.exceptions
import logging.handlers

default_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
fh = logging.handlers.RotatingFileHandler('/var/log/pyNotifications/rabbit_connector.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(default_formatter)

logger = logging.getLogger('pynotifications_rabbit_connector')
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)


class RabbitConnector(pynotifications.connector.Connector):
    def __init__(self, url, queue_name):
        super(RabbitConnector, self).__init__(url=url, queue_name=queue_name)
        self.connection: pika.BlockingConnection = None
        self.channel: pika.adapters.blocking_connection.BlockingChannel = None
        self.setup_connection()

    def create_connection(self):
        parameters = pika.URLParameters(self.url)

        self.connection = pika.BlockingConnection(parameters)

        self.channel = self.connection.channel()

    def declare_queue(self):
        self.channel.queue_declare(queue=self.queue_name, durable=True)

    def push_to_queue(self, data: Dict):
        try:
            self.channel.publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(data),
                properties=pika.BasicProperties(
                    delivery_mode=2
                ),
            )
            logger.info('pushed to queue')
        except pika.exceptions.ConnectionClosed as e:
            logger.exception("connectionClosed - push to queue: %s", e, exc_info=True)
            self.setup_connection()
            self.push_to_queue(data)
        except pika.exceptions.ChannelClosed as e:
            logger.exception("channelClosed - push to queue: %s", e, exc_info=True)
            self.setup_connection()
            self.push_to_queue(data)

    def start_consuming(self, function_to_run: Callable):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(function_to_run, queue=self.queue_name)
        logger.info(' [*] Waiting for messages. To exit press CTRL+C')
        try:
            self.channel.start_consuming()
        except pika.exceptions.ConnectionClosed as e:
            logger.exception("connectionClosed: %s", e, exc_info=True)
            self.setup_connection()
            self.channel.start_consuming()
        except Exception as e:
            logger.exception("Unknown exception: %s", e, exc_info=True)
            self.setup_connection()
            self.channel.start_consuming()