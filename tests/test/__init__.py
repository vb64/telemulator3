"""Root class for testing."""
import os
import unittest
import telebot


class Bot(telebot.TeleBot):
    """Bot instance for tests."""

    def __init__(self):
        """Telebot is parent."""
        super().__init__('xxx-yyy-zzz', threaded=False)
        self.name = 'Test bot'
        self.username = 'bot-username'


class TestCase(unittest.TestCase):
    """Inherit unittest."""

    def setUp(self):
        """Set up tests."""
        super().setUp()

        from telemulator3 import Telemulator

        self.telemul = Telemulator()
        self.telemul.set_tested_bot(Bot())
        self.telemul.api.file_store_path = os.path.join('tests', 'file_store')
        self.api = self.telemul.api

        self.telemul.api.emulate_start()

    def tearDown(self):
        """Clean."""
        self.telemul.api.emulate_stop()
        super().tearDown()
