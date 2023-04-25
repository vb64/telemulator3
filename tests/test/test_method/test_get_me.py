"""Telemulator API GetMe method.

make test T=test_method/test_get_me.py
"""
from . import TestMethod


class TestGetMe(TestMethod):
    """Test for getMe method."""

    def test_response(self):
        """Method call."""
        from telemulator3.method.getMe import response

        code, data = response(self.api, '', {})
        assert code == 200
        assert data["ok"]
        assert data["result"]["is_bot"]

    def test_bot(self):
        """Bot method."""
        user = self.telemul.bot.get_me()
        assert user.is_bot
        assert user.username == 'bot-username'
        assert user.first_name == 'Test bot'
