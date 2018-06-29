import app.connector
from typing import Dict, Type


class Producer:

    def __init__(
            self,
            url: str,
            queue_name: str,
            connector_cls: Type[app.connector.Connector],
            callback_url: str
    ):
        self.connection_mgr = connector_cls(url=url, queue_name=queue_name)
        self.connection_mgr.setup_connection()
        self.callback_url = callback_url

    def _send(self, data: Dict):
        self.connection_mgr.push_to_queue(data=data)

    def formatter(self, **kwargs):
        raise NotImplementedError()

    def send(self, **kwargs):
        self._send(data=self.formatter(**kwargs))