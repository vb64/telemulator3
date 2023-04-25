# pylint: disable=invalid-name
"""Module for forwardMessage method emulator."""
from . import get_chat, get_int, message_to_dic, EmulatorException, error


def response(api, _uri, params):
    """Forward message from the from_chat_id to chat_id and return True."""
    # print "#forwardMessage params", params
    try:
        chat = get_chat(api, params)
    except EmulatorException as exc:
        return error(exc.code, exc.note)

    message_id = get_int(params, 'message_id')
    from_chat_id = get_int(params, 'from_chat_id')
    from_chat = api.bot_chats.get(from_chat_id, None)

    bot = api.get_me()
    message = from_chat.history.messages[message_id]

    ret = bot.forward(from_chat, chat, message)

    return (200, message_to_dic(ret))
