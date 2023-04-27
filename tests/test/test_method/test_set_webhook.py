"""Telemulator API SetWebhook method.

make test T=test_method/test_set_webhook.py
"""
from . import TestMethod


class TestCaseSetWebhook(TestMethod):
    """Test for SetWebhook method."""

    def test_dflt(self):
        """Test method call."""
        answer = self.bot.set_webhook(url='www.xxx.yyy')
        assert answer is True
