"""Telemulator API getChatAdministrators method.

make test T=test_method/test_get_chat_administrators.py
"""
from . import TestMethod


class TestgetChatAdministrators(TestMethod):
    """heck getChatAdministrators method.

    get_chat_administrators(
      chat_id
    )
    """

    def test_dflt(self):
        """Return list of the chat admins."""
        answer = self.bot.get_chat_administrators(self.private.id)
        assert len(answer) == 2

        answer = self.bot.get_chat_administrators(self.group.id)
        assert len(answer) == 1
