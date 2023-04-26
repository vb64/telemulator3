"""Telemulator API.

make test T=test_api.py
"""
import json
from datetime import datetime

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
        from telemulator3.api import emulate_file

        func = emulate_file(self.api)
        request = MockHttprettyRequest('z', path='data/test01.txt')

        answer = func(request, '', self.headers)
        assert answer[0] == 200
        assert answer[-1] == b'test content'

        self.telemul.print_trace(True)
        answer = func(request, '', self.headers)
        assert answer[-1] == b'test content'
        assert answer[0] == 200
        self.telemul.print_trace(False)

    def test_emulate_bot(self):
        """Emulate_bot call."""
        from telemulator3.api import emulate_bot

        self.api.answers[self.method] = (self.code, self.data)
        func = emulate_bot(self.api)

        url = self.telemul.bot.token + '/{}?xxx'.format(self.method)
        answer = func('get', url)
        assert answer.status_code == 200

        url = self.telemul.bot.token + '/{}'.format(self.method)
        answer = func('get', url)
        assert answer.status_code == 200

        self.telemul.print_trace(True)
        assert answer.status_code == 200
        self.telemul.print_trace(False)

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
        code, data = self.api.get_answer('getMe', '', {}, {})
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

        from telemulator3.update.callback_query import CallbackQuery

        call = CallbackQuery(user, 'xxx', chat, message)
        assert self.api.send_update(chat, user, history_item, message=message, callback_query=call)

    def test_create_bot(self):
        """Call create_bot must return user with is_bot == True."""
        assert self.api.create_bot('Test', 'test_bot').is_bot
