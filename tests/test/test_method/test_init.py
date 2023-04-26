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
