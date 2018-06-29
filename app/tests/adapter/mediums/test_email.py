import unittest
from unittest import mock
from app.adapters.mediums import email
from app import exceptions


class TestEmailSchema(unittest.TestCase):

    def setUp(self):
        ...

    def test_invalid_input(self):
        with mock.patch.object(email.medium.Medium, '__init__', return_value=None) as mock_method:
            e = email.Email()
            e.schema = e.default_schema
            self.assertRaises(exceptions.SchemaError, e.validate_data, data={})

    def test_valid_input_without_cc_and_bcc(self):
        with mock.patch.object(email.medium.Medium, '__init__', return_value=None) as mock_method:
            e = email.Email()
            e.schema = e.default_schema
            self.assertIsNone(e.validate_data(data={
                "from": {"address": "", "name": ""},
                "to": {"address": "", "name": ""},
                "subject": "",
                "message": {"text": "", "html": ""}
            }))

    def test_invalid_input_with_cc_and_bcc(self):
        with mock.patch.object(email.medium.Medium, '__init__', return_value=None) as mock_method:
            e = email.Email()
            e.schema = e.default_schema
            self.assertRaises(exceptions.SchemaError, e.validate_data, data={
                "from": {"address": "", "name": ""},
                "to": {"address": "", "name": ""},
                "subject": "",
                "message": {"text": "", "html": ""},
                "cc": "",
                "bcc": ""
            })

    def test_valid_input_with_cc_and_bcc(self):
        with mock.patch.object(email.medium.Medium, '__init__', return_value=None) as mock_method:
            e = email.Email()
            e.schema = e.default_schema
            self.assertIsNone(e.validate_data(data={
                "from": {"address": "", "name": ""},
                "to": {"address": "", "name": ""},
                "subject": "",
                "message": {"text": "", "html": ""},
                "cc": [{"address": ""}],
                "bcc": [{"address": ""}]
            }))


if __name__ == '__main__':
    unittest.main()