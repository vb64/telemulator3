"""Module for getChat method emulator."""
from . import with_chat


@with_chat
def response(_api, _params, chat):
    """Return chat info."""
    # print "#getChat params", _params
    return chat.to_dict()
