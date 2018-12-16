import pynotifications.connector
from typing import Dict, Type, Callable
from pynotifications import utilities
import pynotifications.exceptions
import logging.handlers

default_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
fh = logging.handlers.RotatingFileHandler('/var/log/pyNotifications/consumer.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(default_formatter)

logger = logging.getLogger("pynotifications")
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)


class Consumer:
    """

    """
    def __init__(
            self, url: str, queue_name: str, connector_cls: Type[pynotifications.connector.Connector],
            process_task_function: Callable, call_on_success: bool, call_on_failure: bool
    ):
        self.connection_mgr = connector_cls(url=url, queue_name=queue_name)
        self.connection_mgr.setup_connection()
        self.on_success_hooks = [self.success_callback]
        self.on_failure_hooks = [self.failure_callback, self.push_to_failed_queue]
        self._internal_call_data: Dict = {}
        self.success_callback_url: str = None
        self.failure_callback_url: str = None
        self.callback_data: Dict = None
        self.process_task_function: Callable = process_task_function
        self.failed_tasks_connection_mgr = connector_cls(url=url, queue_name=f"{queue_name}_failed")
        self.failed_tasks_connection_mgr.setup_connection()
        self.deserialized_data = None
        self.call_on_success = call_on_success
        self.call_on_failure = call_on_failure
        self.call_on_completion_override = False
        self.this_call_on_success = None
        self.this_call_on_failure = None
        logger.info("consumer created")

    def start(self):
        self.connection_mgr.start_consuming(function_to_run=self.consume)

    def process_task(self, context: Dict):
        response = self.process_task_function(context)
        logger.info(f"Process task - response: {response}")
        return response

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
        self.deserialized_data = data
        self.success_callback_url = data["success_callback_url"]
        self.failure_callback_url = data["failure_callback_url"]
        self.callback_data = data["callback_data"]
        if data.get("call_on_completion", None) is not None:
            self.call_on_completion_override = True
            self.this_call_on_success = data["call_on_completion"].get("on_success", self.call_on_success)
            self.this_call_on_failure = data["call_on_completion"].get("on_failure", self.call_on_failure)
        else:
            self.call_on_completion_override = False

        return self.process_task(context=data["context"])

    def consume(self, *args, **kwargs):
        try:
            self._internal_call_data = {
                'args': args,
                'kwargs': kwargs
            }
            response = self.call_process_task_with_deserialized_data(*args, **kwargs)
            logger.info(f"RESPONSE: {response}")
            self.on_success(response)
        except (pynotifications.exceptions.ResponseNot200, pynotifications.exceptions.NoConnection) as e:
            self.on_failure(f"data: {e.message}, status_code: {e.status_code}")
        except Exception as e:
            try:
                error = str(e)
            except Exception:
                error = "NOT PROVIDED"
            self.on_failure(error)
        finally:
            self.acknowledge()

    def callback(self, data: Dict, url: str, response):
        try:
            utilities.post(url=url, data={**data, '__response__': response}, json=False)
            logger.info(f'callback successful to: {url} with data {data}')
        except (pynotifications.exceptions.ResponseNot200, pynotifications.exceptions.NoConnection) as e:
            logger.exception(f'callback failed to {url} with data: {data} %s', e, exc_info=1)

    def success_callback(self, response):
        if self.call_on_completion_override:
            should_callback = self.this_call_on_success
        else:
            should_callback = self.call_on_success
        if should_callback:
            self.callback(data=self.callback_data, response=response, url=self.success_callback_url)

    def failure_callback(self, e):
        if self.call_on_completion_override:
            should_callback = self.this_call_on_failure
        else:
            should_callback = self.call_on_failure
        if should_callback:
            self.callback(data=self.callback_data, url=self.failure_callback_url, response=e)

    def acknowledge(self):
        raise NotImplementedError()

    def on_success(self, response):
        logger.info(f"job succeeded, response: {response}")
        for hook in self.on_success_hooks:
            hook(response)

    def on_failure(self, e):
        logger.info(f"job failed")
        for hook in self.on_failure_hooks:
            hook(e)

    def push_to_failed_queue(self, e):
        logger.info(f"pushed job to failed queue, error: {e}")
        self.failed_tasks_connection_mgr.push_to_queue(self.deserialized_data)
