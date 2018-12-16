from typing import Callable, Dict


class Connector:
    """
    This abstract class defines methods for operations with a PubSub system including
        -> creating a connection
        -> creating queue for tasks
        -> publishing tasks to the queue
        -> consuming tasks from the queue
    """
    def __init__(self, url, queue_name):
        self.url = url
        self.queue_name = queue_name

    def setup_connection(self):
        """
        This should be run to get Connector going.
        :return:
        """
        self.create_connection()
        self.declare_queue()

    def create_connection(self):
        """
        This should create a connection and store it in an instance variable
        :return:
        """
        raise NotImplementedError()

    def declare_queue(self):
        """
        This should create/declare a queue for the tasks
        :return:
        """
        raise NotImplementedError()

    def push_to_queue(self, data: Dict):
        """
        This should publish the task to the declared queue
        :param data:
        :return:
        """
        raise NotImplementedError()

    def start_consuming(self, function_to_run: Callable):
        """
        This should start a blocking consumer which will be polling the queues for tasks
        :param function_to_run:
        :return:
        """
        raise NotImplementedError()

