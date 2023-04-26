# pylint: disable=invalid-name
"""Module for sendPhoto method emulator."""
from ..update.message import Photo
from . import message_for_chat, get


@message_for_chat
def response(api, params, chat, reply_to_message, reply_markup):
    """Send photo to chat and return result message.

    How access to file upload data?
    """
    # print "#sendPhoto params", params
    return chat.send(
      Photo(
        chat,
        api.get_me(),
        get(params, 'caption'),
        100, 100, 500,
        reply_to_message=reply_to_message
      ),
      reply_markup=reply_markup
    )
