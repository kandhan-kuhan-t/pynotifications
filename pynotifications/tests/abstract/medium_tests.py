import unittest
from unittest.mock import MagicMock, patch
from pynotifications import medium
from pynotifications import app_types


class TestAbstractConnector(unittest.TestCase):
    def setUp(self):
        self.consumer_class_mock = MagicMock()
        self.issubclass_patcher = patch('pynotifications.medium.issubclass')
        self.issubclass = self.issubclass_patcher.start()
        self.issubclass.return_value = True

    def tearDown(self):
        self.issubclass_patcher.stop()

    def test_init(self):
        m = medium.Medium(
            consumer_class=self.consumer_class_mock, queue_name="queue", broker_url="broker",
            http_call_url="http", http_headers={}, call_on_success=False, call_on_failure=False,
            content_type_is_json=True, schema=None
        )
        self.issubclass.assert_called_with(self.consumer_class_mock, app_types.ConsumerImplementation)
        self.consumer_class_mock.assert_called_with(
            url="broker", queue_name="queue", process_task_function=m.send,
            call_on_success=False, call_on_failure=False
        )


if __name__ == '__main__':
    unittest.main(verbosity=1)