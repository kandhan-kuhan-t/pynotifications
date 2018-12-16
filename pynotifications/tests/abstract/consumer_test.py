import unittest.mock
from pynotifications import consumer


class ConsumerDeserializeDataTest(unittest.TestCase):
    def setUp(self):
        self.connector = unittest.mock.MagicMock()
        self.process_task_function = unittest.mock.MagicMock()
        self.consumer = consumer.Consumer(
            url="url",
            queue_name="queue",
            connector_cls=self.connector,
            process_task_function=self.process_task_function,
            call_on_failure=True,
            call_on_success=True
        )
        self.consumer.process_task = unittest.mock.MagicMock()

    def test_deserialize_data_no_override_call_on_completion(self):
        self.consumer.deserialize_data = unittest.mock.MagicMock(return_value={
            "success_callback_url": "",
            "failure_callback_url": "",
            "callback_data": {},
            "context": {}
        })
        self.consumer.call_process_task_with_deserialized_data()
        self.assertFalse(self.consumer.call_on_completion_override)
        self.assertTrue(self.consumer.call_on_success)
        self.assertTrue(self.consumer.call_on_failure)

    def test_deserialize_data_override_call_on_completion(self):
        self.consumer.deserialize_data = unittest.mock.MagicMock(return_value={
            "success_callback_url": "",
            "failure_callback_url": "",
            "callback_data": {},
            "call_on_completion": {
                "on_success": False,
                "on_failure": False
            },
            "context": {}
        })
        self.consumer.call_process_task_with_deserialized_data()
        self.assertTrue(self.consumer.call_on_completion_override)
        self.assertFalse(self.consumer.this_call_on_success)
        self.assertFalse(self.consumer.this_call_on_failure)


if __name__ == '__main__':
    unittest.main(verbosity=1)