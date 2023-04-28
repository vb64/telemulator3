"""Module for sendDocument method emulator."""
from ..update.message import Document
from . import message_for_chat, get


@message_for_chat
def response(api, params, chat, reply_to_message, reply_markup):
    """Send document to chat and return result message."""
    # print "#sendDocument params", params
    return chat.send(
      Document(
        chat,
        api.get_me(),
        'readme.txt',
        500,
        caption=get(params, 'caption'),
        reply_to_message=reply_to_message
      ),
      reply_markup=reply_markup
    )
