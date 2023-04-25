# pylint: disable=invalid-name
"""Module for leaveChat method emulator."""
from . import with_chat


@with_chat
def response(api, _params, chat):
    """Delete bot from the chat members."""
    # print "#leaveChat params", params
    del api.bot_chats[chat.id]
    del chat.members[api.bot.id]

    return True
