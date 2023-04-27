"""Telemulator API SendAudio method.

make test T=test_method/test_send_audio.py
"""
from . import TestMethod


class TestSendAudio(TestMethod):
    """Test for SendAudio method.

    send_audio(
      chat_id,
      audio,
      caption=None,
      duration=None,
      performer=None,
      title=None,
      reply_to_message_id=None,
      reply_markup=None,
      parse_mode=None,
      disable_notification=None,
      timeout=None
    )
    """

    def test_private(self):
        """Send audio to private chat."""
        # print('###')
        # self.telemul.print_trace(True)
        caption = 'image caption'
        message = self.bot.send_audio(
          self.private.id, 'test.mp3', caption=caption, reply_to_message_id=None,
          reply_markup=None, parse_mode=None, disable_notification=None
        )
        assert message.chat.id == self.private.id
        assert len(self.private.history.messages) == 1
        assert self.private.history.contain('audio ')
        # self.private.history.dump()
