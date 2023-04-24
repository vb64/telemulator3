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

    def process_new_updates(self, updates):
        """Process Telegram API updates."""
        for update in updates:
            print('#', update)


class TestCase(unittest.TestCase):
    """Inherit unittest."""

    def setUp(self):
        """Set up tests."""
        super().setUp()

        from telemulator3 import Telemulator

        self.telemul = Telemulator()
        self.telemul.set_tested_bot(Bot())
        self.telemul.api.file_store_path = os.path.join('tests', 'file_store')
