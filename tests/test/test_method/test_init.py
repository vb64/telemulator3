"""Telemulator API methods support functions.

make test T=test_method/test_init.py
"""
import pytest
from . import TestMethod


class TestInit(TestMethod):
    """Test __init__.py module."""

    def test_error(self):
        """Check error function."""
        from telemulator3.method import error

        code, data = error(100, 'xxx')
        assert code == 100
        assert data['ok'] is False
        assert data['error_code'] == 100
        assert data['description'] == 'xxx'

    def test_get_chat(self):
        """Check get_chat function."""
        from telemulator3.method import get_chat, EmulatorException

        with pytest.raises(EmulatorException) as err:
            get_chat(self.api, {})
        assert "no chat_id" in str(err)

        with pytest.raises(EmulatorException) as err:
            get_chat(self.api, {'chat_id': 666})
        assert "Forbidden:" in str(err)

    def test_with_chat(self):
        """Check with_chat decorator."""
        from telemulator3.method import with_chat

        deco = with_chat(None)
        code, data = deco(None, '', {})
        assert code == 400
        assert data['ok'] is False
        assert 'no chat_id' in data['description']

    def test_message_for_chat(self):
        """Check message_for_chat decorator."""
        from telemulator3.method import message_for_chat

        deco = message_for_chat(None)
        code, data = deco(self.api, '', {'chat_id': 666})
        assert code == 403
        assert data['ok'] is False
        assert 'Forbidden:' in data['description']

        params = {
          'chat_id': list(self.api.chats.keys())[0],
          'reply_to_message_id': 666,
        }
        code, data = deco(self.api, '', params)
        assert code == 402
        assert data['ok'] is False
        assert 'Wrong reply_to_message_id:' in data['description']
