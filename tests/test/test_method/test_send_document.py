"""Telemulator API SendDocument method.

make test T=test_method/test_send_document.py
"""
from . import TestMethod


class TestSendDocument(TestMethod):
    """Test for SendDocument method.

    send_document(
      chat_id,
      data,
      reply_to_message_id=None,
      caption=None,
      reply_markup=None,
      parse_mode=None,
      disable_notification=None,
      timeout=None
    )
    """

    def test_private(self):
        """Send document to private chat."""
        caption = 'document caption'
        message = self.bot.send_document(
          self.private.id, 'file content', caption=caption, reply_to_message_id=None,
          reply_markup=None, parse_mode=None, disable_notification=None, timeout=None
        )

        assert message.chat.id == self.private.id
        assert len(self.private.history.messages) == 1
        assert self.private.history.contain('document readme.txt (500 bytes)')

        caption1 = 'document1 caption'
        self.bot.send_document(
          self.private.id, 'file content', caption=caption1, reply_to_message_id=message.message_id
        )
        # self.private.history.dump()
