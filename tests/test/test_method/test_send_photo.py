"""Telemulator API SendPhoto method.

make test T=test_method/test_send_photo.py
"""
import os
from . import TestMethod


class TestSendPhoto(TestMethod):
    """Test for SendPhoto method.

    send_photo(
      chat_id,
      photo,
      caption=None,
      reply_to_message_id=None,
      reply_markup=None,
      parse_mode=None,
      disable_notification=None
    )
    """

    file_path = os.path.join('tests', 'file_store', 'test01.txt')

    def test_private(self):
        """Test photo to private chat."""
        caption = 'image caption'
        message = self.bot.send_photo(
          self.private.id, open(self.file_path, 'rb'), caption=caption, reply_to_message_id=None,
          reply_markup=None, parse_mode=None, disable_notification=None
        )
        assert message.chat.id == self.private.id
        assert len(self.private.history.messages) == 1
        assert self.private.history.contain(caption)

        caption1 = 'image1 caption'
        self.bot.send_photo(
          self.private.id, open(self.file_path, 'rb'),
          caption=caption1, reply_to_message_id=message.message_id
        )
