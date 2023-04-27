"""Telemulator API DeleteMessage method.

make test T=test_method/test_edit_message_text.py
"""
from telebot.types import InlineKeyboardButton
from . import TestMethod


class TestEditMessageText(TestMethod):
    """Check EditMessageText method.

    def edit_message_text(
      text,
      chat_id=None,
      message_id=None,
      inline_message_id=None,
      parse_mode=None,
      disable_web_page_preview=None,
      reply_markup=None
    )
    """

    def test_private(self):
        """Check EditMessageText in private chat."""
        message = self.bot.send_message(self.private.id, "Hi!")
        assert len(self.private.history.messages) == 1
        assert self.private.history.contain("Hi!")

        self.bot.edit_message_text("Hello!", self.private.id, message.message_id)

        assert len(self.private.history.messages) == 1
        assert not self.private.history.contain("Hi!")
        assert self.private.history.contain("Hello!")

        from telemulator3.update.markup import InlineKeyboard, KeyboardMarkup

        inline = InlineKeyboard()
        inline.row(InlineKeyboardButton("Goto web", url="www.site.com"))

        self.bot.edit_message_text("Hihi!", self.private.id, message.message_id, reply_markup=inline)
        assert len(self.private.history.messages) == 1
        assert self.private.history.contain("www.site.com")

        self.bot.edit_message_text(
          "Haha!",
          self.private.id,
          message.message_id,
          reply_markup=KeyboardMarkup()
        )
        assert len(self.private.history.messages) == 1
        assert not self.private.history.contain("www.site.com")
        # self.private.history.dump()
