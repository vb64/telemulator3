"""Chat keyboards.

make test T=test_chat/test_keyboard.py
"""
import pytest
from telebot.types import (
   ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, ReplyKeyboardRemove
)
from . import TestChat


class TestKeyboard(TestChat):
    """Test chat keyboard."""

    def setUp(self):
        """Create keyboard fro tests."""
        super().setUp()
        from telemulator3.chat.keyboard import Keyboard
        from telemulator3.user import User

        self.keyboard = Keyboard(self.private)
        self.bot = User.from_bot(self.api)

    def test_tg_button(self):
        """Check tg_button function."""
        from telemulator3.update.message import Text

        markup = ReplyKeyboardMarkup()
        markup.row(KeyboardButton('Yes'), KeyboardButton('No'))
        chat = self.private
        user = self.teleuser

        chat.keyboard.assign(Text(chat, self.bot, 'Hello!'), markup)

        chat.history.clear()
        chat.keyboard.menu_item(user, 0)
        assert chat.history.contain('Yes')

        chat.history.clear()
        chat.keyboard.menu_item(user, 1)
        assert chat.history.contain('No')

        chat.history.clear()
        chat.keyboard.menu_item(user, 0)
        assert chat.history.contain('Yes')

    def test_inline(self):
        """Test handle inline markup."""
        from telemulator3.update.message import Text
        from telemulator3.update.markup import InlineKeyboard

        message = Text(self.private, self.bot, 'Hello!')
        inline = InlineKeyboard()
        inline.row(InlineKeyboardButton("Goto web", url="www.site.com"))

        self.keyboard.assign(message, inline)
        assert self.keyboard.menu_size() == 0
        assert message.buttons
        assert '[Goto web](url: www.site.com)' in str(message)

    def test_default(self):
        """Test Keyboard class of the chat."""
        from telemulator3 import EmulatorException
        from telemulator3.update.message import Text

        markup = ReplyKeyboardMarkup()
        markup.row(KeyboardButton('Yes'), KeyboardButton('No'))
        markup.row(KeyboardButton('Maybe'))
        chat = self.private
        user = self.teleuser

        message_user = Text(chat, user, 'Hello from {}!'.format(user))
        message_bot = Text(chat, self.bot, 'Hello! from {}'.format(self.bot))

        with pytest.raises(EmulatorException) as err:
            self.keyboard.assign(message_user, markup)
        assert "Try to set reply_markup" in str(err)

        self.keyboard.assign(message_bot, markup)
        self.keyboard.dump()

        assert self.keyboard.menu_size() == 3

        chat.history.clear()
        self.keyboard.menu_item(user, 0)
        chat.history.contain('Yes')

        chat.history.clear()
        self.keyboard.menu_item(user, 1)
        chat.history.contain('No')

        chat.history.clear()
        self.keyboard.menu_item(user, -1)
        chat.history.contain('No')

        chat.history.clear()
        self.keyboard.menu_item(user, 0, row=1)
        chat.history.contain('Maybe')

        with pytest.raises(IndexError) as err:
            self.keyboard.menu_item(user, 100)
        assert "list index out of range" in str(err)

        assert self.keyboard.contain('May')
        assert not self.keyboard.contain('NoNo')

        self.keyboard.assign(message_bot, ReplyKeyboardRemove())
        assert not self.keyboard.markup
        assert not self.keyboard.contain('NoNo')

        with pytest.raises(EmulatorException) as err:
            self.keyboard.menu_item(user, 100)
        assert "Custom menu not set" in str(err)

        assert self.keyboard.menu_size() == 0

        with pytest.raises(EmulatorException) as err:
            self.keyboard.assign(message_bot, 666)
        assert "Unknown type of reply_markup:" in str(err)

    def test_one_time_keyboard(self):
        """Test Keyboard and ReplyKeyboardMarkup with one_time_keyboard=True."""
        from telemulator3.update.message import Text

        chat = self.private
        user = self.teleuser
        markup = ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.row(KeyboardButton('Yes'), KeyboardButton('No'))
        self.keyboard.assign(Text(chat, self.bot, 'Hello!'), markup)

        assert self.keyboard.menu_size() == 2

        chat.history.clear()
        self.keyboard.menu_item(user, 0)
        chat.history.contain('Yes')

        assert self.keyboard.menu_size() == 0
        self.keyboard.dump()  # need for coverage!

    def test_bot(self):
        """Test Keyboard from message from the bot."""
        markup = ReplyKeyboardMarkup()
        markup.row(KeyboardButton('Yes'), KeyboardButton('No'))
        chat = self.private

        chat.history.clear()
        self.api.bot.send_message(chat.id, 'Hello!', reply_markup=markup)

        assert chat.history.contain('Hello!')
        assert chat.keyboard.contain('Yes')
        assert chat.keyboard.contain('No')
        assert chat.keyboard.menu_size() == 2
        # chat.history.dump()
        # chat.keyboard.dump()
