import pynotifications.consumer
from pynotifications import app_types, utilities
from typing import Type, Dict
from schema import Schema, Or, SchemaError
import pynotifications.exceptions


class Medium:
    def __init__(
            self,
            consumer_class: Type[app_types.ConsumerImplementation],
            queue_name: str,
            broker_url: str,
            http_call_url: str,
            http_headers: Dict,
            call_on_success: bool,
            call_on_failure: bool,
            content_type_is_json: bool=True,
            schema=None,
    ):
        if not issubclass(consumer_class, app_types.ConsumerImplementation):
            raise Exception()
        self.consumer: pynotifications.consumer.Consumer = consumer_class(
            url=broker_url, queue_name=queue_name, process_task_function=self.send,
            call_on_success=call_on_success, call_on_failure=call_on_failure
        )
        self.schema = schema
        self.request_parameters_schema = Schema(
            {
                "url": str,
                "headers": Or(dict, None),
                "data": dict
            }
        )
        self.call_url = http_call_url
        self.headers = http_headers
        self.content_type_is_json = content_type_is_json
        self.response_text = None

    def validate_data(self, data):
        try:
            self.schema.validate(data)
        except SchemaError as e:
            raise pynotifications.exceptions.SchemaError(",".join(e.autos))

    def as_consumer(self) -> pynotifications.consumer.Consumer:
        return self.consumer

    def send(self, data: Dict):
        self.response_text = None
        self.validate_data(data)
        request_dict = self.create_request_parameters(data)
        # self.request_parameters_schema.validate(request_dict)
        response = utilities.post(
            **request_dict,
            json=self.content_type_is_json
        )
        return response

    def format_data(self, data: Dict) -> Dict:

        raise NotImplementedError()

    def create_request_parameters(self, data: Dict) -> Dict:
        request_params = {
            "url": self.call_url,
            "headers": self.headers,
            "data": self.format_data(data)
        }
        return request_params
