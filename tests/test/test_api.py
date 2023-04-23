"""Telemulator API.

make test T=test_api.py
"""
import json
import httpretty
from . import TestCase


class MockHttprettyRequest:
    """Mock httpretty request."""

    def __init__(self, querystring):
        """Set querystring property."""
        self.querystring = querystring


class TestApi(TestCase):
    """Telemulator API."""

    method = 'testMethod'
    code = 200
    data = 'testMethodData'
    headers = {}
    answer = (code, headers, json.dumps(data))

    def test_emulate_bot_get(self):
        """Emulate_bot with GET method."""
        from telemulator3.api import emulate_bot

        self.telemul.api.answers[self.method] = (self.code, self.data)
        func = emulate_bot(self.telemul.api, httpretty.GET)

        url = self.telemul.bot.token + '/{}?xxx'.format(self.method)
        assert func(MockHttprettyRequest('zzz'), url, self.headers) == self.answer

        url = self.telemul.bot.token + '/{}'.format(self.method)
        assert func(MockHttprettyRequest('zzz'), url, self.headers) == self.answer

    def test_debug_print(self):
        """Check debug print."""
        from telemulator3 import api

        save = api.DEBUG_PRINT
        api.DEBUG_PRINT = True

        self.telemul.api.answers[self.method] = (self.code, self.data)
        func = api.emulate_bot(self.telemul.api, httpretty.GET)

        url = self.telemul.bot.token + '/{}'.format(self.method)
        assert func(MockHttprettyRequest('zzz'), url, self.headers) == self.answer

        api.DEBUG_PRINT = save

    def test_fix_ampersand(self):
        """Function fix_ampersand."""
        from telemulator3.api import HTTPRETTY_AMPERSAND, fix_ampersand

        assert fix_ampersand(['1' + HTTPRETTY_AMPERSAND + '2']) == ['1&2']
        assert fix_ampersand(['123']) == ['123']
