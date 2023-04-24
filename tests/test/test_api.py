"""Telemulator API.

make test T=test_api.py
"""
import json
import httpretty
from . import TestCase


class MockHttprettyRequest:
    """Mock httpretty request."""

    def __init__(self, querystring, parsed_body=None, headers=None, body='', path=''):
        """Set querystring property."""
        self.querystring = querystring
        self.parsed_body = parsed_body or {}
        self.headers = headers or {}
        self.body = body
        self.path = path


class TestApi(TestCase):
    """Telemulator API."""

    method = 'testMethod'
    code = 200
    data = 'testMethodData'
    headers = {}
    answer = (code, headers, json.dumps(data))

    def test_emulate_file(self):
        """Function emulate_file."""
        from telemulator3.api import emulate_file, debug_print

        func = emulate_file(self.telemul.api, httpretty.GET)
        request = MockHttprettyRequest('z', path='data/test01.txt')

        answer = func(request, '', self.headers)
        assert answer[0] == 200
        assert answer[-1] == b'test content'

        debug_print(True)
        answer = func(request, '', self.headers)
        assert answer[-1] == b'test content'
        assert answer[0] == 200
        debug_print(False)

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

        request.headers['Content-Type'] = 'multipart/form-data; boundary=*****'
        request.body = """
--*****
Content-Disposition: form-data; name="value1"
Content-Type: text/plain; charset=UTF-8

f0ef73c5-54dd-40cf-9ee7-5c4cb764eb28
--*****
        """
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

    def test_get_file(self):
        """Method get_file must return 200 if custom_file_content set."""
        save = self.telemul.api.file_store_path
        self.telemul.api.file_store_path = None

        code, data = self.telemul.api.get_file('not_exist')
        assert code == 200
        assert data == "file content stub"

        self.telemul.api.custom_file_content = 'zzz'
        code, data = self.telemul.api.get_file('not_exist')
        assert code == 200
        assert data == 'zzz'
        self.telemul.api.custom_file_content = None

        self.telemul.api.file_store_path = save

        code, data = self.telemul.api.get_file('not_exist')
        assert code == 400
        assert 'No such file or directory' in data

        code, data = self.telemul.api.get_file('test01.txt')
        assert code == 200
        assert 'test content' in data.decode('utf-8')

        self.telemul.api.file_store_path = None
