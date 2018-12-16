from typing import Dict
from schema import Schema
from pynotifications import medium


class SMS(medium.Medium):
    def __init__(
            self,
            schema=None,
            **kwargs
    ):
        default_schema = Schema(
            {
                "from": {
                    "number": str,
                },
                "to": {
                    "number": str
                },
                "message": str,
            }
        )
        _schema = schema if schema is not None else default_schema
        super(SMS, self).__init__(schema=_schema, **kwargs)

    def format_data(self, data: Dict) -> Dict:

        raise NotImplementedError()

