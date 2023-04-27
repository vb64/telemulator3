"""Telemulator API getChatMeberCount method.

make test T=test_method/test_get_chat_member_count.py
"""
import pytest
from telebot.apihelper import ApiException

from . import TestMethod


class TestMeberCount(TestMethod):
    """Check getChatMeberCount method.

    get_chat_members_count(
      chat_id
    )
    """

    def test_private(self):
        """Return members count of given chat."""
        answer = self.bot.get_chat_members_count(self.private.id)
        assert answer == len(self.private.members)

        answer = self.bot.get_chat_members_count(self.group.id)
        assert answer == len(self.group.members)

        with pytest.raises(ApiException) as err:
            self.bot.get_chat_members_count(666)
        assert "Forbidden" in str(err)
