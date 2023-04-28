"""Module for sendMessage method emulator."""
from ..update.message import Text
from . import EmulatorException, message_for_chat, get


@message_for_chat
def response(api, params, chat, reply_to_message, reply_markup):
    """Send text to chat and return result message."""
    # print "#sendMessage params", params
    if 'text' not in params:
        raise EmulatorException(402, "Wrong request no text: {}".format(params))

    return chat.send(
      Text(
        chat,
        api.get_me(),
        get(params, 'text'),
        reply_to_message=reply_to_message
      ),
      reply_markup=reply_markup
    )
