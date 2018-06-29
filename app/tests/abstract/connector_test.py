import unittest
from unittest.mock import create_autospec
from app import connector


class TestAbstractConnector(unittest.TestCase):
    def setUp(self):
        self.original = connector.Connector(url="", queue_name="")
        self.mock = connector.Connector(url="", queue_name="")
        self.mock.create_connection = create_autospec(self.mock.create_connection)
        self.mock.declare_queue = create_autospec(self.mock.declare_queue)

    def test_not_implemented_methods(self):
        c = self.original
        self.assertRaises(NotImplementedError, c.create_connection)
        self.assertRaises(NotImplementedError, c.push_to_queue, data=None)
        self.assertRaises(NotImplementedError, c.start_consuming, function_to_run=None)
        self.assertRaises(NotImplementedError, c.declare_queue)

    def test_setup_connection_calls_methods(self):
        c = self.mock
        c.setup_connection()
        c.create_connection.assert_called_once()
        c.declare_queue.assert_called_once()


if __name__ == '__main__':
    unittest.main(verbosity=1)