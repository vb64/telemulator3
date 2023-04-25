"""Telemulator API.

make test T=test_api.py
"""
import json
from datetime import datetime
import httpretty

from telebot.types import Message
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

        func = emulate_file(self.api, httpretty.GET)
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

        func = emulate_bot(self.api, httpretty.POST)
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

        self.api.answers[self.method] = (self.code, self.data)
        func = emulate_bot(self.api, httpretty.GET)

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
        save = self.api.file_store_path
        self.api.file_store_path = None

        code, data = self.api.get_file('not_exist')
        assert code == 200
        assert data == "file content stub"

        self.api.custom_file_content = 'zzz'
        code, data = self.api.get_file('not_exist')
        assert code == 200
        assert data == 'zzz'
        self.api.custom_file_content = None

        self.api.file_store_path = save

        code, data = self.api.get_file('not_exist')
        assert code == 400
        assert 'No such file or directory' in data

        code, data = self.api.get_file('test01.txt')
        assert code == 200
        assert 'test content' in data.decode('utf-8')

        self.api.file_store_path = None

    def test_get_answer(self):
        """Method get_answer."""
        code, data = self.api.get_answer('getMe', '', {})
        assert code == 200
        assert data['ok']
        assert data["result"]["is_bot"]

    def test_get_date_int(self):
        """Method get_date_int."""
        assert self.api.get_date_int()

    def test_get_date(self):
        """Method get_date."""
        date = datetime.now()
        self.api.custom_date = date
        assert self.api.get_date() == date

    def test_get_me(self):
        """Method get_me."""
        bot = self.api.get_me()
        assert bot.id == 1
        assert self.api.get_me().id == 1

    def test_send_update(self):
        """Call for send_update must put history_item to the history of appropriate chat."""
        user = self.api.create_user('Test')
        chat = user.private()
        message = Message(111, user, self.api.get_date(), chat, "json", {}, '')
        history_item = (message.message_id, message)

        self.api.send_update(chat, user, history_item, message=message)
        assert message.message_id in chat.history.messages

        chat.history.clear()

        self.api.send_update(None, None, history_item, message=message)
        assert message.message_id not in chat.history.messages
        assert not chat.history.messages

        assert self.api.send_update(chat, self.api.get_me(), history_item, message=message) is None

    def test_create_bot(self):
        """Call create_bot must return user with is_bot == True."""
        assert self.api.create_bot('Test', 'test_bot').is_bot
