"""Telemulator API GetMe method.

make test T=test_method/test_get_me.py
"""
from . import TestMethod


class TestGetMe(TestMethod):
    """Test for getMe method."""

    def test_dflt(self):
        """Method call."""
        from telemulator3.method.getMe import response

        code, data = response(self.telemul.api, '', {})
        assert code == 200
        assert data["ok"]
        assert data["result"]["is_bot"]
