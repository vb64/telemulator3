"""Module for class, that represented ReplyKeyboard for Telegram chat."""
from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup

from .. import EmulatorException  # pylint: disable=cyclic-import
from ..update.message import Text


class Keyboard:
    """Class for Telegram chat custom keyboard."""

    def __init__(self, chat):
        """Create keyboard for chat."""
        self.markup = None
        self.chat = chat

    def assign(self, message, reply_markup):
        """Set chat keyboard."""
        if reply_markup is None:
            return

        if not (message.from_user and message.from_user.is_bot):
            raise EmulatorException(
              "Try to set reply_markup to {} by not bot: '{}'.".format(self, message.from_user)
            )

        if isinstance(reply_markup, ReplyKeyboardRemove):
            self.markup = None
        elif isinstance(reply_markup, ReplyKeyboardMarkup):
            self.markup = reply_markup
        elif isinstance(reply_markup, InlineKeyboardMarkup):
            reply_markup.attach(message)
        else:
            raise EmulatorException("Unknown type of reply_markup: {}.".format(reply_markup))

    def contain(self, substring):
        """Check for is any menu item contains substring."""
        if not self.markup:
            return False

        for row in self.markup.keyboard:
            for col in row:
                if substring in col['text']:
                    return True

        return False

    def dump(self):
        """Print chat keyboard."""
        if not self.markup:
            return

        print("==========")
        for row in self.markup.keyboard:
            for col in row:
                text = "[{}]".format(col['text'])
                print(text)
            print()

    def menu_item(self, from_user, col, row=0):
        """Send to chat keyboard item value, specified by row and column indexes."""
        if not self.markup:
            raise EmulatorException("Custom menu not set.")

        text = self.markup.keyboard[row][col]['text']

        if self.markup.one_time_keyboard:
            self.markup = None

        return self.chat.send(Text(self.chat, from_user, text))

    def menu_size(self):
        """Return total number of items in the keyboard."""
        if not self.markup:
            return 0

        return sum([len(row) for row in self.markup.keyboard])  # pylint: disable=consider-using-generator
