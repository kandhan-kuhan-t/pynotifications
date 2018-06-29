import app.consumer
import json
from app.adapters.connectors.rabbit import RabbitConnector
from typing import Callable
from app import app_types


class RabbitConsumer(app.consumer.Consumer):

    def __init__(self, url: str, queue_name: str, process_task_function: Callable, **kwargs):
        self.connector_cls = RabbitConnector
        self.connection_mgr: RabbitConnector = None  # For type hinting only
        super().__init__(
            connector_cls=self.connector_cls, url=url, queue_name=queue_name,
            process_task_function=process_task_function,
            **kwargs
        )

    def deserialize_data(self, channel, method, properties, body, *args, **kwargs):
        data = json.loads(body)
        return data

    def acknowledge(self):
        self.connection_mgr.channel.basic_ack(self._internal_call_data["args"][1].delivery_tag)


app_types.ConsumerImplementation.register(RabbitConsumer)
