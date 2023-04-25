# pylint: disable=invalid-name
"""Module for editMessageText method emulator."""
from telebot.types import InlineKeyboardMarkup
from ..update.message import Text
from ..update import markup
from . import with_chat, get, get_int, get_json


@with_chat
def response(api, params, chat):
    """Replace text and markup for given chat message."""
    # print "#editMessageText params", params
    message_id = get_int(params, 'message_id')
    reply_markup = markup.from_dict(get_json(params, 'reply_markup'))

    message = Text(
      chat,
      api.get_me(),
      get(params, 'text')
    )
    if isinstance(reply_markup, InlineKeyboardMarkup):
        reply_markup.attach(message)

    chat.history.messages[message_id] = message

    return True
