"""Root class for testing."""
import unittest


class Bot:
    """Bot instance for tests."""

    name = 'Test bot'
    username = 'bot-username'
    token = 'xxx-yyy-zzz'

    def process_new_updates(self, update_list):
        """Process Telegram API updates."""
        for update in update_list:
            print('#', update)


class TestCase(unittest.TestCase):
    """Inherit unittest."""

    def setUp(self):
        """Set up tests."""
        super().setUp()

        from telemulator3 import Telemulator
        self.telemul = Telemulator()
        self.telemul.set_tested_bot(Bot())
