"""Telemulator API GetChat method.

make test T=test_method/test_get_chat.py
"""
from . import TestMethod


class TestGetChat(TestMethod):
    """Check GetChat method.

    get_chat(
      chat_id
    )
    """

    def test_private(self):
        """Return chat info."""
        answer = self.bot.get_chat(self.private.id)
        assert answer.id == self.private.id

        answer = self.bot.get_chat(self.group.id)
        assert answer.title == self.group.title
