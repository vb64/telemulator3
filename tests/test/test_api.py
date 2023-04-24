"""Telemulator API.

make test T=test_api.py
"""
import json
import httpretty
from . import TestCase


class MockHttprettyRequest:
    """Mock httpretty request."""

    def __init__(self, querystring, parsed_body=None, headers=None):
        """Set querystring property."""
        self.querystring = querystring
        self.parsed_body = parsed_body or {}
        self.headers = headers or {}


class TestApi(TestCase):
    """Telemulator API."""

    method = 'testMethod'
    code = 200
    data = 'testMethodData'
    headers = {}
    answer = (code, headers, json.dumps(data))

    def test_emulate_bot_post(self):
        """Emulate_bot with POST method."""
        from telemulator3.api import emulate_bot

        func = emulate_bot(self.telemul.api, httpretty.POST)
        url = self.telemul.bot.token + '/{}'.format(self.method)
        request = MockHttprettyRequest(
          'zzz',
          parsed_body={
            'text': 'test text',
            'other_key': 'otherkey data'
          }
        )
        assert func(request, url, self.headers)[0] == 400

    def test_emulate_bot_get(self):
        """Emulate_bot with GET method."""
        from telemulator3.api import emulate_bot, debug_print

        self.telemul.api.answers[self.method] = (self.code, self.data)
        func = emulate_bot(self.telemul.api, httpretty.GET)

        url = self.telemul.bot.token + '/{}?xxx'.format(self.method)
        assert func(MockHttprettyRequest('zzz'), url, self.headers) == self.answer

        url = self.telemul.bot.token + '/{}'.format(self.method)
        assert func(MockHttprettyRequest('zzz'), url, self.headers) == self.answer

        debug_print(True)
        assert func(MockHttprettyRequest('zzz'), url, self.headers) == self.answer
        debug_print(False)

    def test_fix_ampersand(self):
        """Function fix_ampersand."""
        from telemulator3.api import HTTPRETTY_AMPERSAND, fix_ampersand

        assert fix_ampersand(['1' + HTTPRETTY_AMPERSAND + '2']) == ['1&2']
        assert fix_ampersand(['123']) == ['123']
