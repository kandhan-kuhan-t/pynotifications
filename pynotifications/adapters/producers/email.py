import pynotifications.producer
from typing import List
import logging.handlers

default_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
fh = logging.handlers.RotatingFileHandler('/var/log/pyNotifications/email.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(default_formatter)

logger = logging.getLogger("email")
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)


class Email(pynotifications.producer.Producer):

    def send(
            self,
            from_name: str,
            from_address: str,
            to_name: str,
            to_address: str,
            subject: str,
            message_html: str,
            message_text: str,
            callback_data,
            cc_addresses: List[str]=None,
            bcc_addresses: List[str]=None,
    ):
        super().send(**{var: val for var, val in locals().items() if var!='self'})

    def formatter(self, **kwargs):
        logger.info(f"EmailProducer: {kwargs}")
        o = {
            "context": {
                "from": {
                    "name": kwargs.get("from_name"),
                    "address": kwargs.get("from_address")
                },
                "to": {
                    "name": kwargs.get("to_name"),
                    "address": kwargs.get("to_address")
                },
                "subject": kwargs.get("subject"),
                "message": {
                    "html": kwargs.get("message_html"),
                    "text": kwargs.get("message_text")
                }
            },
            "success_callback_url": self.callback_url,
            "failure_callback_url": self.callback_url,
            "callback_data": kwargs.get("callback_data")
        }
        cc_addresses = kwargs.get('cc_addresses')
        bcc_addresses = kwargs.get('bcc_addresses')
        if cc_addresses:
            o['context']["cc"] = [{'address': cc_address} for cc_address in cc_addresses]
        if bcc_addresses:
            o['context']["bcc"] = [{'address': bcc_address} for bcc_address in bcc_addresses]
        logger.info(f"EmailProducer-Formatted: {o}")
        return o