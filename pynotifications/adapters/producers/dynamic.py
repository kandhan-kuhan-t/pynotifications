import pynotifications.producer
from typing import Dict


class DynamicProducer(pynotifications.producer.Producer):

    def send(
            self,
            post_data: Dict,
            callback_data: Dict,
            url: str,
            headers: Dict,
            is_json: bool,
            call_on_completion: Dict=None,
    ):
        super().send(**{var:val for var, val in locals().items() if var != 'self'})

    def formatter(self, **kwargs):
        return {
            "context": {
                "post_data": kwargs.get("post_data"),
                "url": kwargs.get("url"),
                "headers": kwargs.get("headers"),
                "is_json": kwargs.get("is_json")
            },
            "success_callback_url": self.callback_url + "/success",
            "failure_callback_url": self.callback_url + "/failure",
            "callback_data": kwargs.get("callback_data"),
            "call_on_completion": kwargs.get("call_on_completion", None),
        }
