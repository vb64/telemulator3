"""Module for deleteMessage method emulator."""
from . import with_chat, get_int


@with_chat
def response(_api, params, chat):
    """Delete message from the chat and return True."""
    # print "#deleteMessage params", params
    message_id = get_int(params, 'message_id')
    if message_id in chat.history.messages:
        del chat.history.messages[message_id]

    return True
