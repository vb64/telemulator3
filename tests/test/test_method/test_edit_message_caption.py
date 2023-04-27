"""Telemulator API EditMessageCaption method.

make test T=test_method/test_edit_message_caption.py
"""
from telebot.types import InlineKeyboardButton
from . import TestMethod


class TestEditMessageCaption(TestMethod):
    """Check EditMessageCaption method.

    def edit_message_caption(
      caption,
      chat_id=None,
      message_id=None,
      inline_message_id=None,
      parse_mode=None,
      reply_markup=None
    )
    """

    def test_private(self):
        """Edit messages caption in private chat."""
        caption = 'image caption'
        message = self.bot.send_photo(self.private.id, 'file content', caption=caption)
        assert message.chat.id == self.private.id
        assert len(self.private.history.messages) == 1
        assert self.private.history.contain(caption)

        caption1 = 'image1 caption'

        self.bot.edit_message_caption(caption1, self.private.id, message.message_id)
        assert len(self.private.history.messages) == 1
        assert not self.private.history.contain(caption)
        assert self.private.history.contain(caption1)

        from telemulator3.update.markup import InlineKeyboard
        inline = InlineKeyboard()
        inline.row(InlineKeyboardButton("Goto web", url="www.site.com"))

        # print('###')
        # self.telemul.print_trace(True)
        self.bot.edit_message_caption(caption1, self.private.id, message.message_id, reply_markup=inline)
        assert self.private.history.contain("www.site.com")
        # self.private.history.dump()
