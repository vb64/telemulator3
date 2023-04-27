"""Group chat.

make test T=test_chat/test_group.py
"""
import pytest
from . import TestChat


class TestGroup(TestChat):
    """Test group chat."""

    def test_set_admin(self):
        """Check set_admin."""
        from telemulator3.chat import MemberStatus

        user = self.teleuser
        group = user.create_group("New Group")
        assert group.members[user.id].status == MemberStatus.Creator

        group.set_admin(user)
        assert group.members[user.id].status == MemberStatus.Administrator

        user2 = self.api.create_user('Another')
        group.set_admin(user2)
        assert group.members[user2.id].status == MemberStatus.Administrator

    def test_messages(self):
        """Test send messages of various types to group."""
        from telemulator3 import EmulatorException
        from telemulator3.update.message import Text

        user = self.teleuser
        group = user.create_group("Test group")

        group.send(Text(group, user, "send text"))
        assert len(group.history.messages) == 1
        assert group.history.contain("send text")

        with pytest.raises(EmulatorException) as err:
            group.send(Text(group, self.api.create_user('Another'), "send text"))
        assert "is not member of group" in str(err)

        user1 = self.api.create_user('Another')

        with pytest.raises(EmulatorException) as err:
            group.add_members(user1, [])
        assert "not a member of group" in str(err)

        with pytest.raises(EmulatorException) as err:
            group.add_members(user, [])
        assert "try to add empty member list" in str(err)

    def test_add_members(self):
        """Bot cant join group by invite link."""
        from telemulator3 import EmulatorException

        group = self.teleuser.create_group("Test group")
        with pytest.raises(EmulatorException) as err:
            group.add_members(None, [self.api.get_me()])
        assert "can't join" in str(err)
        assert "by invite link" in str(err)
