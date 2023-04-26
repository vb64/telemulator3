"""Telemulator API answerCallbackQuery method.

make test T=test_method/test_answer_callback_query.py
"""
import pytest
from telebot.apihelper import ApiException
from telebot.types import InlineKeyboardButton
from . import TestMethod


class TestAnswerCallbackQuery(TestMethod):
    """Check AnswerCallbackQuery method.

    def answer_callback_query(
      callback_query_id,
      text=None,
      show_alert=None,
      url=None,
      cache_time=None
    )
    """

    def test_private(self):
        """Test answer for callback_query in private chat."""
        from telemulator3.update.markup import InlineKeyboard

        user = self.api.create_user('TestCallback')
        private = user.private()

        inline = InlineKeyboard()
        inline.row(InlineKeyboardButton("Run callback", callback_data="call_xxx"))

        self.bot.send_message(private.id, "Hi!", reply_markup=inline)
        assert len(private.history.messages) == 1
        assert private.history.contain("Hi!")

        callback_query = inline.tap(user, 0)
        assert not user.notifications.messages
        assert callback_query.from_user.id == user.id

        assert self.bot.answer_callback_query(callback_query.id, "Callback OK")
        assert len(user.notifications.messages) == 1
        user.notifications.dump()  # need for coverage

        assert self.bot.answer_callback_query(callback_query.id, "")
        assert len(user.notifications.messages) == 1

        callback_query.from_user = None
        assert self.bot.answer_callback_query(callback_query.id, "OK")

        with pytest.raises(ApiException) as err:
            self.bot.answer_callback_query(666, "")
        assert "Wrong callback_query_id:" in str(err)
