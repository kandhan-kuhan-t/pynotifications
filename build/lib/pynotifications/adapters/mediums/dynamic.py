import pynotifications.consumer
from pynotifications import app_types, utilities
from typing import Type, Dict
from schema import Schema, Or
import pynotifications.exceptions


class Medium:
    def __init__(
            self,
            consumer_class: Type[app_types.ConsumerImplementation],
            queue_name: str,
            broker_url: str,
            call_on_success: bool,
            call_on_failure: bool,
    ):
        if not issubclass(consumer_class, app_types.ConsumerImplementation):
            raise Exception()

        self.consumer: pynotifications.consumer.Consumer = consumer_class(
            url=broker_url, queue_name=queue_name, process_task_function=self.send,
            call_on_success=call_on_success, call_on_failure=call_on_failure
        )
        self.request_parameters_schema = Schema(
            {
                "url": str,
                "headers": Or(dict, None),
                "data": dict
            }
        )

    def validate_data(self, data):
        ...

    def as_consumer(self) -> pynotifications.consumer.Consumer:
        return self.consumer

    def send(self, data: Dict):
        self.validate_data(data)
        request_dict = self.create_request_parameters(data=data["post_data"], url=data["url"], headers=data["headers"])
        self.request_parameters_schema.validate(request_dict)
        return utilities.post(
            **request_dict,
            json=data["is_json"]
        )

    def format_data(self, data: Dict) -> Dict:
        return data

    def create_request_parameters(self, data: Dict, url: str, headers: Dict) -> Dict:
        request_params = {
            "url": url,
            "headers": headers,
            "data": self.format_data(data)
        }
        return request_params
