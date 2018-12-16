from adapters.mediums.sms import SMS
import base64
from typing import Dict


class Twilio(SMS):

    def __init__(
            self,
            http_headers=None,
            http_call_url="https://api.twilio.com/2010-04-01/Accounts/AC5bde2f121fa7d5ea59f4c53dcddc1e3e/Messages",
            content_type_is_json=False,
            **kwargs
    ):
        if http_headers is None:
            http_headers = { "Authorization":
              f"Basic {base64.b64encode(b'AC5bde2f121fa7d5ea59f4c53dcddc1e3e:c6686f8ad0294857513a1bcf1f7efb95').decode('utf-8')}"
            }
        super().__init__(
            http_call_url=http_call_url,
            http_headers=http_headers,
            content_type_is_json=content_type_is_json,
            **kwargs
        )

    def format_data(self, data) -> Dict:
        return {
            "To": data["to"]["number"],
            "From": data["from"]["number"],
            "Body": data["message"]
        }
