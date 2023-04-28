"""Module for getChatMemberCount method emulator."""
from . import with_chat


@with_chat
def response(_api, _params, chat):
    """Return chat members count."""
    # print "#getChatMemberCount params", params
    return len(chat.members)
