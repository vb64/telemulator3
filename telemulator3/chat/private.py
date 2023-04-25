"""Module for class, that represented Telegram private chat."""
from .. import EmulatorException  # pylint: disable=cyclic-import
from . import Type, MemberStatus
from .base import Chat
from .member import ChatMember


class Private(Chat):
    """Class, that represented of Telegram private chat.

    Raise exception, if private chat for creator already exist
    """

    def __init__(self, creator, **kwargs):
        """Create new private chat."""
        if creator.id in creator.api.chats:
            raise EmulatorException(
              "Try to create existing private: {}".format(creator.api.chats[creator.id])
            )

        super().__init__(
          self,
          creator,
          Type.Private,
          title=creator.full_name(),
          **kwargs
        )
        creator.api.bot_chats[self.id] = self
        bot = creator.api.get_me()
        self.members = {
          creator.id: ChatMember(creator, MemberStatus.Creator),
          bot.id: ChatMember(bot, MemberStatus.Creator),
        }

    def add_members(self, _chat_admin, _members):
        """Adding users to private chat not allowed."""
        raise EmulatorException("Attempt to add members to the private chat: '{}'".format(self.title))
