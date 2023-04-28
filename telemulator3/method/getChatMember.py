"""Module for getChatMember method emulator."""
from ..chat import MemberStatus
from ..chat.member import ChatMember
from . import with_chat, get_int


@with_chat
def response(api, params, chat):
    """Return chat members count."""
    # print "#getChatMember params", params
    user_id = get_int(params, 'user_id')
    member = chat.members.get(user_id, None)
    if not member:
        user = api.users.get(user_id, {'id': user_id, 'is_bot': False, 'first_name': '???'})
        member = ChatMember(user, MemberStatus.Left)

    return member.to_dict()
