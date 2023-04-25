# pylint: disable=invalid-name
"""Module for editMessageReplyMarkup method emulator."""
from ..update import markup
from . import with_chat, get_int, get_json


@with_chat
def response(_api, params, chat):
    """Replace text and markup for given chat message."""
    # print "#editMessageReplyMarkup.py params", params
    message_id = get_int(params, 'message_id')
    reply_markup = markup.from_dict(get_json(params, 'reply_markup'))

    message = chat.history.messages.get(message_id, None)
    if message:
        reply_markup.attach(message)
        return True

    return False