"""Channel chat.

make test T=test_chat/test_channel.py
"""
import pytest
from . import TestChat


class TestChannel(TestChat):
    """Test channel."""

    def test_messages(self):
        """Test send messages to channel."""
        from telemulator3 import EmulatorException
        from telemulator3.update.message import Text

        user = self.teleuser
        channel = user.create_channel("Test channel")

        channel.send(Text(channel, user, "send text"))
        assert len(channel.history.messages) == 1
        assert channel.history.contain("send text")

        user1 = self.api.create_user('Another')

        with pytest.raises(EmulatorException) as err:
            channel.send(Text(channel, user1, "send text"))
        assert "is not member of channel" in str(err)

        user1.join(channel)

        with pytest.raises(EmulatorException) as err:
            channel.send(Text(channel, user1, "send text"))
        assert "try to send message to channel" in str(err)

    def test_check_can_write(self):
        """Test check_can_write for system service mrssage."""
        channel = self.teleuser.create_channel("Test channel")
        assert channel.check_can_write(None) is None
