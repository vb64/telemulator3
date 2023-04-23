"""Telemulator properties.

make test T=test_init.py
"""
import os
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

    def test_clean_proxy(self):
        """Bot clean_proxy method."""
        os.environ['http_proxy'] = 'xxx'
        assert 'http_proxy' in os.environ
        self.telemul.clean_proxy()
        assert 'http_proxy' not in os.environ
