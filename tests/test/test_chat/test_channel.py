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
        """Test check_can_write for system service message."""
        channel = self.teleuser.create_channel("Test channel")
        assert channel.check_can_write(None) is None

    def test_add_admin(self):
        """Test add_admin."""
        from telemulator3 import EmulatorException

        channel = self.teleuser.create_channel("Test channel")
        user = self.api.create_user('Another')

        with pytest.raises(EmulatorException) as err:
            channel.add_admin(None, user)
        assert "can't join" in str(err)
        assert "by invite link" in str(err)

        bot = self.api.get_me()
        assert len(self.api.bot_chats) == 1
        channel.add_admin(self.teleuser, bot)
        assert len(self.api.bot_chats) == 2

        channel.members[self.teleuser.id].can_promote_members = False
        with pytest.raises(EmulatorException) as err:
            channel.add_admin(self.teleuser, user)
        assert "does not has rights to set new admins" in str(err)

        channel.members[self.teleuser.id].can_promote_members = True
        channel.add_admin(self.teleuser, user)
        assert len(channel.members) == 3

    def test_add_members(self):
        """Test add_members."""
        from telemulator3 import EmulatorException

        channel = self.teleuser.create_channel("Test channel")

        with pytest.raises(EmulatorException) as err:
            channel.add_members(self.teleuser, [self.api.get_me()])
        assert "Try to add bot" in str(err)
        assert "as member" in str(err)
