"""Telemulator API DeleteMessage method.

make test T=test_method/test_delete_message.py
"""
from . import TestMethod


class TestDeleteMessage(TestMethod):
    """Check DeleteMessage method.

    delete_message(
      chat_id,
      message_id
    )
    """

    def test_dflt(self):
        """Remove message from chat history."""
        from telemulator3.update.message import Text

        message = Text(self.private, self.user, 'Hello!')
        self.private.send(message)

        assert len(self.private.history.messages) == 1

        answer = self.bot.delete_message(self.private.id, message.message_id)
        assert answer is True
        assert not self.private.history.messages

        answer = self.bot.delete_message(self.private.id, message.message_id)
        assert answer is True
        assert not self.private.history.messages
