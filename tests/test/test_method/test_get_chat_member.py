"""Telemulator API getChatMember method.

make test T=test_method/test_get_chat_member.py
"""
from . import TestMethod


class TestChatMember(TestMethod):
    """Check getChatMember method.

    get_chat_member(
      chat_id,
      user_id
    )
    """

    def test_dflt(self):
        """Return data for member of chat."""
        from telemulator3.chat import MemberStatus

        answer = self.bot.get_chat_member(self.private.id, self.teleuser.id)
        assert answer.status == MemberStatus.Creator

        answer = self.bot.get_chat_member(self.group.id, self.bot.id)
        assert answer.status == MemberStatus.Member

        answer = self.bot.get_chat_member(self.group.id, 666)
        assert answer.status == MemberStatus.Left
