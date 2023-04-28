"""Module for getChatAdministrators method emulator."""
from ..chat import MemberStatus
from . import with_chat


@with_chat
def response(_api, _params, chat):
    """Return chat admin list."""
    # print "#getChatAdministrators params", _params
    return [
      member.to_dict() for member in chat.members.values()
      if member.status in [
        MemberStatus.Creator,
        MemberStatus.Administrator,
      ]
    ]
