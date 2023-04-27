"""Base clas for chats.

make test T=test_chat/test_base.py
"""
import pytest
from . import TestChat


class TestBase(TestChat):
    """Test base class of chats."""

    def test_signed_message(self):
        """Test chat with signed_message."""
        from telemulator3.update.message import Text
        from telemulator3 import EmulatorException

        chat = self.teleuser.create_channel("Test channel")
        chat.signed_message = True
        assert not chat.history.messages

        msg = chat.send(Text(chat, self.teleuser, "send text"))
        assert len(chat.history.messages) == 1
        assert 'Test User' in msg.author_signature

        chat.members[self.teleuser.id].can_invite_users = False
        with pytest.raises(EmulatorException) as err:
            chat.check_add_members_rigts(self.teleuser, [])
        assert "does not has rights to invite" in str(err)
