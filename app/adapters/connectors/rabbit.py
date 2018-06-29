from typing import Callable, Dict
import app.connector
import json
import pika
from logging import getLogger

logger = getLogger('local')


class RabbitConnector(app.connector.Connector):
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
        self.channel.publish(
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(data),
            properties=pika.BasicProperties(
                delivery_mode=2
            ),
        )
        logger.info('pushed to queue')

    def start_consuming(self, function_to_run: Callable):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(function_to_run, queue=self.queue_name)
        logger.info(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()
