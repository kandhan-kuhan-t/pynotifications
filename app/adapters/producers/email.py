import app.producer


class Email(app.producer.Producer):

    def send(
            self,
            from_name: str,
            from_address: str,
            to_name: str,
            to_address: str,
            subject: str,
            message_html: str,
            message_text: str,
            callback_data
    ):
        super().send(**{var:val for var, val in locals().items() if var!='self'})

    def formatter(self, **kwargs):
        return {
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