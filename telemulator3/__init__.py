"""Mocked elements of the Telegram Bot API for unit tests."""
import os


class EmulatorException(Exception):
    """This class represents an Exception thrown when a call to the Emulator fails."""


class Telemulator:
    """Class for Telegram API tests."""

    api = None
    teleuser = None
    private = None
    group = None
    tele_message = None
    group_message = None

    def set_tested_bot(self, bot):
        """Set bot for testing.

        The bot must have follows properties and methods:

        - name: bot name
        - username: bot username
        - token: bot API token
        - process_new_updates([update]): method for process Telegram API update
        """
        from .api import Telegram

        self.clean_proxy()
        self.api = Telegram(bot)

    @property
    def bot(self):
        """Shortcut for tested bot."""
        return self.api.bot

    @staticmethod
    def clean_proxy():
        """Remove system proxy settings.

        Its need for correct proccesing httpretty + requests
        """
        for proxy in ['https_proxy', 'http_proxy']:
            if proxy in os.environ:
                del os.environ[proxy]

    @staticmethod
    def print_trace(is_on):
        """Switch printing calls to Telegram API."""
        from .api import debug_print
        debug_print(is_on)

    @staticmethod
    def create_group(title, from_user, members=None):
        """Create Telegram group and set it as supergroup."""
        from .chat import Type

        group = from_user.create_group(title)
        group.type = Type.Supergroup
        if members:
            group.add_members(from_user, members)

        return group

    def create_channel(self, title, from_user, add_bot=True):
        """Xreate Telegram channel and add bot to it as channel admin."""
        channel = from_user.create_channel(title)
        if add_bot:
            channel.add_admin(from_user, self.api.bot)

        return channel
