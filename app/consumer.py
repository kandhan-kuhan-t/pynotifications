import app.connector
from typing import Dict, Type, Callable
from app import utilities
import app.exceptions
from logging import getLogger

logger = getLogger("local")


class Consumer:
    """

    """
    def __init__(
            self, url: str, queue_name: str, connector_cls: Type[app.connector.Connector],
            process_task_function: Callable
    ):
        self.connection_mgr = connector_cls(url=url, queue_name=queue_name)
        self.connection_mgr.setup_connection()
        self.on_success_hooks = [self.success_callback]
        self.on_failure_hooks = [self.failure_callback]
        self._internal_call_data: Dict = {}
        self.success_callback_url: str = None
        self.failure_callback_url: str = None
        self.callback_data: Dict = None
        self.process_task_function: Callable = process_task_function
        logger.info("consumer created")

    def start(self):
        self.connection_mgr.start_consuming(function_to_run=self.consume)

    def process_task(self, context: Dict):
        return self.process_task_function(context)

    def deserialize_data(self, *args, **kwargs) -> Dict:
        """

        :param args:
        :param kwargs:
        :return: {
            "success_callback_url": str,
            "failure_callback_url": str,
            "callback_data": Dict,
            "context: Dict
        }
        """
        raise NotImplementedError()

    def call_process_task_with_deserialized_data(self, *args, **kwargs):
        data: Dict = self.deserialize_data(*args, **kwargs)
        self.success_callback_url = data["success_callback_url"]
        self.failure_callback_url = data["failure_callback_url"]
        self.callback_data = data["callback_data"]
        self.process_task(context=data["context"])

    def consume(self, *args, **kwargs):
        try:
            self._internal_call_data = {
                'args': args,
                'kwargs': kwargs
            }
            self.call_process_task_with_deserialized_data(*args, **kwargs)
            self.on_success()
        except Exception as e:
            self.on_failure(e)
        finally:
            self.acknowledge()

    def callback(self, data: Dict, url: str):
        try:
            utilities.post(url=url, data=data, json=True)
            logger.info(f'callback successful to: {url} with data {data}')
        except (app.exceptions.ResponseNot200, app.exceptions.NoConnection) as e:
            logger.exception(f'callback failed to {url} with data: {data} %s', e, exc_info=1)

    def success_callback(self):
        self.callback(data=self.callback_data, url=self.success_callback_url)

    def failure_callback(self, e):
        self.callback(data=self.callback_data, url=self.failure_callback_url)

    def acknowledge(self):
        raise NotImplementedError()

    def on_success(self):
        for hook in self.on_success_hooks:
            hook()

    def on_failure(self, e):
        for hook in self.on_failure_hooks:
            hook(e)