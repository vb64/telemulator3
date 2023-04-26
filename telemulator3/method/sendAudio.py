# pylint: disable=invalid-name
"""Module for sendAudio method emulator."""
from ..update.message import Audio
from . import message_for_chat, get


@message_for_chat
def response(api, params, chat, reply_to_message, reply_markup):
    """Send mp3 to chat and return result message."""
    # print "#sendAudio params", params
    return chat.send(
      Audio(
        chat,
        api.get_me(),
        100, 500, 'performer',
        get(params, 'caption'),
        reply_to_message=reply_to_message
      ),
      reply_markup=reply_markup
    )
