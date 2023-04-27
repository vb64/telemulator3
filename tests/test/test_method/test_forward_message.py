"""Telemulator API ForwardMessage method.

make test T=test_method/test_forward_message.py
"""
import pytest
from telebot.apihelper import ApiException
from . import TestMethod


class TestForwardMessage(TestMethod):
    """Check ForwardMessage method.

    forward_message(
      chat_id,
      from_chat_id,
      message_id,
      disable_notification=None
    )
    """

    def test_dflt(self):
        """Forward message from chat history."""
        from telemulator3.update.message import Text

        message = Text(self.group, self.user, 'Hello!')
        self.group.send(message)

        assert len(self.group.history.messages) == 2

        answer = self.bot.forward_message(self.private.id, self.group.id, message.message_id)
        assert answer.forward_from_chat.id == self.group.id
        assert len(self.private.history.messages) == 1

        self.user.stop_bot()
        with pytest.raises(ApiException) as err:
            self.bot.forward_message(self.private.id, self.group.id, message.message_id)
        assert "Forbidden:" in str(err)
