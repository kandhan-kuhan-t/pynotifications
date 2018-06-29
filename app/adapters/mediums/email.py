from typing import Dict
from schema import Schema, Or, Optional
from app import medium


class Email(medium.Medium):
    def __init__(
            self,
            schema=None,
            **kwargs
    ):
        self.default_schema = Schema(
            {
                "from": {
                    "address": str,
                    "name": str
                },
                "to": {
                    "address": str,
                    "name": str
                },
                Optional("cc"): [
                    {
                        "address": str,
                    }
                ],
                Optional("bcc"): [
                    {
                        "address": str
                    }
                ],
                "subject": str,
                "message": {
                    "text": Or(str, None),
                    "html": str
                }
            }
        )
        _schema = schema if schema is not None else self.default_schema
        super().__init__(schema=_schema, **kwargs)

    def format_data(self, data: Dict) -> Dict:

        raise NotImplementedError()
