import unittest
from unittest.mock import MagicMock, patch
from code123 import get_last_email, parse_email, create_calendar_event, main

class TestCode123(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.gmail_service = MagicMock()
        cls.calendar_service = MagicMock()
        cls.event_data = {'subject': 'Test Event', 'body': 'Test Body'}

    @patch('code123.build')
    def test_main(self, mock_build):
        mock_build.return_value.__getitem__.return_value = self.gmail_service
        mock_build.return_value.__getitem__.return_value = self.calendar_service
        main()
        self.gmail_service.users.return_value.messages.return_value.list.assert_called_once()
        self.calendar_service.events.return_value.insert.assert_called_once()

    def test_get_last_email(self):
        result = get_last_email(self.gmail_service)
        self.gmail_service.users.return_value.messages.return_value.list.assert_called_once()
        self.assertEqual(result, self.gmail_service.users.return_value.messages.return_value.list.return_value)

    def test_parse_email(self):
        result = parse_email(self.gmail_service.users.return_value.messages.return_value.list.return_value)
        self.assertEqual(result, self.event_data)

    def test_create_calendar_event(self):
        result = create_calendar_event(self.calendar_service, self.event_data)
        self.calendar_service.events.return_value.insert.assert_called_once()
        self.assertEqual(result, self.calendar_service.events.return_value.insert.return_value)

if __name__ == '__main__':
    unittest.main()
