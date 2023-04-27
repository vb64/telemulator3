"""Telemulator API CallbackQuery update class.

make test T=test_update/test_callback_query.py
"""
from telebot import types
from . import TestUpdate


class TestCallbackQuery(TestUpdate):
    """Tests for Telegram CallbackQuery."""

    def test_init(self):
        """Check string."""
        from telemulator3.update.callback_query import CallbackQuery

        callback_query = CallbackQuery(self.teleuser, 'test_data', str(self.private.id), None)
        assert isinstance(callback_query, types.CallbackQuery)
        assert '>> tap inline button with callback_data: test_data' in str(callback_query)
