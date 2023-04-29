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

    def set_tested_bot(self, bot, username='tested_bot', name='Test Bot'):
        """Set telebot.TeleBot instance for testing."""
        from .api import Telegram

        self.clean_proxy()
        bot.username = username
        bot.name = name
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

    def call_query(self, from_user, callback_data, message):
        """Return CallbackQuery."""
        from .update.callback_query import CallbackQuery

        return CallbackQuery(from_user, callback_data, str(from_user.id), message)

    def callback(self, message, from_user, callback_data):
        """Emulate click on callback button on given message."""
        callback_query = self.call_query(from_user, callback_data, message)
        return self.api.send_update(
          message.chat,
          from_user,
          (message.message_id, callback_query),
          callback_query=callback_query
        )

    def tap_inline_button(self, user, message, button_code):
        """Call callback with mnemonic."""
        return self.callback(message, user, button_code)


# helpers
#########

def send_command(chat, command, from_user, **kwargs):
    """Send command to given chat."""
    from .update.message import Command
    return chat.send(Command(chat, from_user, command, **kwargs))


def private_command(command, from_user, **kwargs):
    """Send command to private chat."""
    return send_command(from_user.private(), command, from_user, **kwargs)


def send_text(chat, text, from_user, **kwargs):
    """Send text to given chat."""
    from .update.message import Text
    return chat.send(Text(chat, from_user, text, **kwargs))


def private_text(text, from_user, **kwargs):
    """Send text to private chat."""
    return send_text(from_user.private(), text, from_user, **kwargs)


def send_document(chat, file_name, from_user, file_size=600, **kwargs):
    """Send document to given chat."""
    from .update.message import Document
    return chat.send(Document(chat, from_user, file_name, file_size, **kwargs))


def private_document(file_name, from_user, file_size=600, **kwargs):
    """Send document to private chat."""
    return send_document(
      from_user.private(), file_name, from_user, file_size=file_size, **kwargs
    )


def send_photo(chat, from_user, caption='caption', width=640, height=480, file_size=500, **kwargs):
    """Send photo to given chat."""
    from .update.message import Photo
    return chat.send(Photo(chat, from_user, caption, width, height, file_size, **kwargs))


def private_photo(from_user, caption='caption', width=640, height=480, file_size=500, **kwargs):
    """Send photo to private chat."""
    return send_photo(
      from_user.private(), from_user, caption=caption,
      width=width, height=height, file_size=file_size, **kwargs
    )


def send_voice(chat, from_user, duration=5, file_size=500, **kwargs):
    """Send voice to given chat."""
    from .update.message import Voice
    return chat.send(Voice(chat, from_user, duration, file_size, **kwargs))


def private_voice(from_user, duration=5, file_size=500, **kwargs):
    """Send voice to private chat."""
    return send_voice(
      from_user.private(), from_user, duration=duration, file_size=file_size, **kwargs
    )


def send_contact(chat, phone_number, from_user, first_name='Contact', last_name='User', user_id=777, **kwargs):
    """Send contact to given chat."""
    from .update.message import Contact
    return chat.send(
      Contact(chat, from_user, phone_number, first_name, last_name, user_id, **kwargs)
    )


def private_contact(phone_number, from_user, first_name='Contact', last_name='User', user_id=777, **kwargs):
    """Send contact to private chat."""
    return send_contact(
      from_user.private(), phone_number, from_user,
      first_name=first_name, last_name=last_name, user_id=user_id, **kwargs
    )
