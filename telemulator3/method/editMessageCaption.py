# pylint: disable=invalid-name
"""Module for editMessageCaption method emulator."""
from telebot.types import InlineKeyboardMarkup

from ..update import markup
from . import with_chat, get_int, get_json, get


@with_chat
def response(_api, params, chat):
    """Replace caption for given chat message."""
    # print "#editMessageCaption params", params
    caption = get(params, 'caption')
    message_id = get_int(params, 'message_id')
    reply_markup = markup.from_dict(get_json(params, 'reply_markup'))

    message = chat.history.messages[message_id]
    message.caption = caption

    if isinstance(reply_markup, InlineKeyboardMarkup):
        reply_markup.attach(message)

    return True