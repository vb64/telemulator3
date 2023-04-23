"""Telemulator properties.

make test T=test_init.py
"""
from . import TestCase


class TestInit(TestCase):
    """Telemulator properties."""

    def test_bot(self):
        """Bot properties."""
        assert self.telemul
        assert self.telemul.bot
        assert self.telemul.bot.name == 'Test bot'
        assert self.telemul.bot.username == 'bot-username'
        assert self.telemul.bot.token == 'xxx-yyy-zzz'
