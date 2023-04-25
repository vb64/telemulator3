# pylint: disable=invalid-name
"""Module for sendMessage method emulator."""
from ..update.message import Text
from . import message_for_chat, get


@message_for_chat
def response(api, params, chat, _reply_to_message, _reply_markup):
    """Send text to chat and return result message."""
    # print "#sendMessage params", params
    return chat.send(
      Text(
        chat,
        api.get_me(),
        get(params, 'action'),
      )
    )
