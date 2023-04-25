"""Module for class of Telegram channel."""
from .. import EmulatorException  # pylint: disable=cyclic-import
from . import Type, MemberStatus
from .base import Chat
from .member import ChatMember


class Channel(Chat):
    """Class, that represented of Telegram Channel."""

    def __init__(self, creator, title, start_message_id=0, **kwargs):
        """Create channel by user."""
        Chat.__init__(
          self, creator, Type.Channel, start_message_id=start_message_id, title=title, **kwargs
        )
        self.signed_message = False
        self.members = {
          creator.id: ChatMember(
            creator, MemberStatus.Creator,
            can_promote_members=True,
            can_post_messages=True,
            can_edit_messages=True,
            can_change_info=True,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True
          )
        }

    def check_can_write(self, user):
        """Raise exception in user not admin member."""
        if not user:
            return

        if user.id not in self.members:
            raise EmulatorException(
              "User '{}' is not member of {} and try to send message to channel.".format(user, self)
            )
        member = self.members[user.id]
        if not member.can_post_messages:
            raise EmulatorException(
              "Member '{}' with status {} try to send message to {}".format(user, member.status, self)
            )

    def add_admin(self, admin, new_admin):
        """Add new channel admin.

        New admin cant join to channel by invite link.
        """
        self.check_add_members_rigts(admin, [new_admin])
        if not admin:
            raise EmulatorException(
              "New chat admin '{}' can't join to {} by invite link".format(new_admin, self)
            )

        if not self.members[admin.id].can_promote_members:
            raise EmulatorException(
              "User '{}' does not has rights to set new admins for {}.".format(admin, self)
            )

        self.members[new_admin.id] = ChatMember(
          new_admin, MemberStatus.Administrator, can_post_messages=True
        )

        if new_admin.id == self.creator.api.bot.id:
            self.creator.api.bot_chats[self.id] = self

    def add_members(self, admin, members):
        """Add users from list 'members' to this channel.

        Bots can be added as admin only. Also bots cant join to channel by invite link.
        """
        self.check_add_members_rigts(admin, members)

        for user in members:
            if user.is_bot:
                raise EmulatorException(
                  "Try to add bot '{}' to {} as member.".format(user, self)
                )
            self.members[user.id] = ChatMember(user, MemberStatus.Member)
