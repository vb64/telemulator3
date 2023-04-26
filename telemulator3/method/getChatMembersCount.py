# pylint: disable=invalid-name
"""Module for getChatMembersCount method emulator."""
from . import with_chat


@with_chat
def response(_api, _params, chat):
    """Return chat members count."""
    # print "#getChatMembersCount params", params
    return len(chat.members)
