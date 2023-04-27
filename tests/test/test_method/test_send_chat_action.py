"""Telemulator API SendChatAction method.

make test T=test_method/test_send_chat_action.py
"""
from . import TestMethod


class TestSendChatAction(TestMethod):
    """Test for SendChatAction method.

    send_chat_action(
      chat_id,
      action
    )
    """

    def test_private(self):
        """Send message to private chat."""
        self.bot.send_chat_action(self.private.id, 'typing')
        assert len(self.private.history.messages) == 1
        assert self.private.history.contain('typing')
        # self.private.history.dump()
