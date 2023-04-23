"""Telemulator API.

make test T=test_api.py
"""
import httpretty
from . import TestCase


class MockHttprettyRequest:
    """Mock httpretty request."""

    def __init__(self, querystring):
        """Set querystring property."""
        self.querystring = querystring


class TestApi(TestCase):
    """Telemulator API."""

    def test_emulate_bot_get(self):
        """Emulate_bot with GET method."""
        from telemulator3.api import emulate_bot

        self.telemul.api.answers['testMethod'] = (200, 'testMethodData')
        func = emulate_bot(self.telemul.api, httpretty.GET)
        url = self.telemul.bot.token + '/' + 'testMethod?xxx'
        assert func(MockHttprettyRequest('zzz'), url, {}) == (200, {}, '"testMethodData"')
