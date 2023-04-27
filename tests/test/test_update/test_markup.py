"""Telemulator API Markup update class.

make test T=test_update/test_markup.py
"""
import pytest
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from . import TestUpdate


class TestMarkup(TestUpdate):
    """Tests for Telegram markup."""

    def test_inline(self):
        """Test types.InlineKeyboardMarkup class."""
        from telemulator3.update.markup import from_dict, dump_inline_button, InlineKeyboard
        from telemulator3.update.message import Text
        from telemulator3 import EmulatorException

        inline = InlineKeyboard()
        inline.row(
          InlineKeyboardButton("Goto web", url="www.site.com"),
          InlineKeyboardButton("Run callback", callback_data="call_xxx"),
        )
        markup = from_dict(inline.to_dict())
        assert isinstance(markup, InlineKeyboardMarkup)

        assert len(markup.keyboard) == 1

        line = dump_inline_button(markup.keyboard[0][0].to_dict())
        assert line == '\n[Goto web](url: www.site.com)'

        line = dump_inline_button(markup.keyboard[0][1].to_dict())
        assert line == '\n[Run callback](callback_data: call_xxx)'

        data = {'wrong_data': True}
        with pytest.raises(EmulatorException) as err:
            dump_inline_button(data)
        assert "Unknown inline button markup type:" in str(err)

        user = self.api.create_user('Test')
        chat = user.private()
        bot = user.api.get_me()

        inline.tap(user, 0)
        assert not chat.history.contain('Goto to url:')

        inline.tap(user, 1)
        assert not chat.history.contain('tap inline button with callback_data: call_xxx')

        chat.keyboard.assign(Text(chat, bot, 'Hello!', ), inline)

        inline.tap(user, 0)
        assert chat.history.contain('Goto to url:')

        inline.tap(user, 1)
        assert chat.history.contain('tap inline button with callback_data: call_xxx')

        # chat.history.dump()

        inline.row(
          InlineKeyboardButton("Not implemented", callback_game="xxx"),
        )
        with pytest.raises(EmulatorException) as err:
            inline.tap(user, 0, row=1)
        assert "Unknown inline button type:" in str(err)

    def test_dflt(self):
        """Test types.ReplyKeyboardRemove class."""
        from telemulator3.update.markup import from_dict
        from telemulator3 import EmulatorException

        data = {
          'remove_keyboard': True
        }
        markup = from_dict(data)
        assert isinstance(markup, ReplyKeyboardRemove)
        data['selective'] = True
        markup = from_dict(data)
        assert markup.selective

        data = {
          'keyboard': [
            [{'text': 'Yes'}, {'text': 'No'}],
          ]
        }
        markup = from_dict(data)
        assert isinstance(markup, ReplyKeyboardMarkup)

        assert not markup.selective
        assert not markup.resize_keyboard
        assert not markup.one_time_keyboard

        data['selective'] = True
        data['resize_keyboard'] = True
        data['one_time_keyboard'] = True
        markup = from_dict(data)
        assert markup.selective
        assert markup.resize_keyboard
        assert markup.one_time_keyboard

        data = {
          'wrong_data': True
        }
        with pytest.raises(EmulatorException) as err:
            from_dict(data)
        assert "Unknown markup type:" in str(err)
