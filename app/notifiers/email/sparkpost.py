from app.adapters.mediums.email import Email
from typing import Dict
from logging import getLogger

logger = getLogger('local')


class SparkPost(Email):

    def __init__(
            self,
            http_headers,
            http_call_url,
            **kwargs
    ):
        super().__init__(
            http_call_url=http_call_url,
            http_headers=http_headers,
            **kwargs
        )

    def format_data(self, data) -> Dict:
        return {
            "recipients": [
                {
                    "address": {
                        "email": data["to"]["address"],
                        "name": data["to"]["name"]
                    }
                }
            ],
            "content": {
                "html": data["message"]["html"],
                "text": data["message"]["text"],
                "subject": data["subject"],
                "from": {
                    "name": data["from"]["name"],
                    "email": data["from"]["address"]
                }
            }
        }
