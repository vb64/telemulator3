"""Module for class of group Telegram chat."""
from .. import EmulatorException  # pylint: disable=cyclic-import
from ..update.message import NewChatMembers
from . import Type, MemberStatus
from .base import Chat
from .member import ChatMember


class Group(Chat):
    """Class, that represented of Telegram group."""

    def __init__(self, creator, title, **kwargs):
        """Create new group."""
        super().__init__(
          self, creator, Type.Group, title=title, **kwargs
        )
        self.members = {
          creator.id: ChatMember(
            creator,
            MemberStatus.Creator,
            can_change_info=True,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_promote_members=True
          )
        }

    def add_members(self, admin, members):
        """Add users from list 'members' to list of the this chat members."""
        self.check_add_members_rigts(admin, members)

        for user in members:
            if user.is_bot and (not admin):
                raise EmulatorException(
                  "Bot '{}' can't join to {} by invite link".format(user, self)
                )
            self.members[user.id] = ChatMember(user, MemberStatus.Member)

            if user.id == self.creator.api.bot.id:
                self.creator.api.bot_chats[self.id] = self

        if self.id in self.creator.api.bot_chats:
            self.send(NewChatMembers(self, admin, members))

    def set_admin(self, user):
        """Sssign user as group admin.

        If user not group member, he join to group
        """
        if user.id not in self.members:
            self.add_members(None, [user])

        self.members[user.id].status = MemberStatus.Administrator
