from pynotifications.adapters.mediums.email import Email
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
        logger.info(f"Sparkpost:incoming - {data}")
        formatted_data = {
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
        ccs = data.get("cc")
        bccs = data.get("bcc")
        if ccs:
            for cc in ccs:
                formatted_data["recipients"].append(
                    {
                        "address": {
                            "email": cc["address"],
                            "header_to": data["to"]["address"]
                        }
                    }
                )
            formatted_data["content"]["headers"] = {
                "CC": ','.join(
                    [
                        cc['address'] for cc in ccs
                    ]
                )
            }

        if bccs:
            for bcc in bccs:
                formatted_data["recipients"].append(
                    {
                        "address": {
                            "email": bcc["address"],
                            "header_to": data["to"]["address"]
                        }
                    }
                )

        return formatted_data
