"""Telemulator API leaveChat method.

make test T=test_method/test_leave_chat.py
"""
from . import TestMethod


class TestLeaveChat(TestMethod):
    """Test for leaveChat method.

    leave_chat(
      chat_id
    )
    """

    def test_dflt(self):
        """Remove bot from chat."""
        assert len(self.group.members) == 2
        answer = self.bot.leave_chat(self.group.id)
        assert answer
        assert len(self.group.members) == 1
