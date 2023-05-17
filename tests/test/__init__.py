"""Root class for testing."""
import os
import unittest
from telebot import TeleBot


class TestCase(unittest.TestCase):
    """Inherit unittest."""

    def setUp(self):
        """Set up tests."""
        super().setUp()

        from telemulator3 import Telemulator

        self.telemul = Telemulator()
        self.telemul.set_tested_bot(
          TeleBot('xxx-yyy-zzz', threaded=False),
          name='Test bot',
          username='bot-username'
        )

        self.api = self.telemul.api
        self.bot = self.api.bot
        self.api.file_store_path = os.path.join('tests', 'file_store')

        assert not self.api.users
        assert self.api.get_me().username == 'bot-username'
        assert len(self.api.users) == 1

        self.teleuser = self.api.create_user('Test', 'User', language_code='en')
        self.private = self.teleuser.private()
        self.group = self.teleuser.create_group("Test group")

        from telemulator3.update.message import Text

        self.tele_message = Text(self.private, self.teleuser, "Hello private!")
        self.group_message = Text(self.group, self.teleuser, "Hello group!")
