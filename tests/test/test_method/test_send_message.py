"""Telemulator API SendMessage method.

make test T=test_method/test_send_message.py
"""
import pytest
from telebot.apihelper import ApiException

from . import TestMethod


class TestSendMessage(TestMethod):
    """Test for SendMessage method.

    send_message(
      chat_id,
      text,
      disable_web_page_preview=None,
      reply_to_message_id=None,
      reply_markup=None,
      parse_mode=None,
      disable_notification=None
    )
    """

    def call_response(self, params):
        """Call function 'response'."""
        from telemulator3.method.sendMessage import response
        return response(self.api, '', params)  # pylint: disable=no-value-for-parameter

    def test_response(self):
        """Test wrong sendMessage calls."""
        params = {}
        code, data = self.call_response(params)
        assert code == 400
        assert 'no chat_id' in data['description']

        params['chat_id'] = '666'
        code, data = self.call_response(params)
        assert code == 403
        assert 'Forbidden:' in data['description']

        params['chat_id'] = self.private.id
        code, data = self.call_response(params)
        assert code == 402
        assert 'Wrong request no text:' in data['description']

    def test_private(self):
        """Test messages to private chat."""
        text = "Hello, API!"
        reply = "Hi!"

        message = self.bot.send_message(self.private.id, text)
        assert message.chat.id == self.private.id
        assert len(self.private.history.messages) == 1
        assert self.private.history.contain(text)

        self.bot.send_message(self.private.id, reply, reply_to_message_id=message.message_id)
        assert len(self.private.history.messages) == 2
        assert self.private.history.contain(">> reply to [")

    def test_group(self):
        """Test messages to group chat."""
        text = "Hello, API!"
        reply = "Hi!"

        message = self.bot.send_message(self.group.id, text)
        assert message.chat.id == self.group.id
        assert len(self.group.history.messages) == 2
        assert self.group.history.contain(text)

        self.bot.send_message(self.group.id, reply, reply_to_message_id=message.message_id)
        assert len(self.group.history.messages) == 3
        assert self.group.history.contain(">> reply to [")

        self.group.history.messages = {}
        with pytest.raises(ApiException) as err:
            self.bot.send_message(self.group.id, reply, reply_to_message_id=message.message_id)
        assert "Wrong reply_to_message_id:" in str(err)
        # self.group.history.dump()
