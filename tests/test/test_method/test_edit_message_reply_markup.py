"""Telemulator API EditMessageReplyMarkup method.

make test T=test_method/test_edit_message_reply_markup.py
"""
from telebot.types import InlineKeyboardButton
from . import TestMethod


class TestEditMessageReplyMarkup(TestMethod):
    """Check EditMessageReplyMarkup method.

    def edit_message_reply_markup(
      chat_id=None,
      message_id=None,
      inline_message_id=None,
      reply_markup=None
    )
    """

    def test_private(self):
        """Check EditMessageReplyMarkup in private chat."""
        message = self.bot.send_message(self.private.id, "Hi!")
        assert len(self.private.history.messages) == 1
        assert self.private.history.contain("Hi!")

        from telemulator3.update.markup import InlineKeyboard
        inline = InlineKeyboard()
        inline.row(InlineKeyboardButton("Goto web", url="www.site.com"))

        self.bot.edit_message_reply_markup(self.private.id, message.message_id, reply_markup=inline)
        assert len(self.private.history.messages) == 1
        assert self.private.history.contain("www.site.com")

        self.private.history.messages = {}
        self.bot.edit_message_reply_markup(self.private.id, message.message_id, reply_markup=inline)
        # self.private.history.dump()
