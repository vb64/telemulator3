"""Module for class, that represented Telegram account."""
from telebot.types import User as UserBase

from . import EmulatorException  # pylint: disable=cyclic-import
from .update.message import LeftChatMember, Text

from .chat import Type, MemberStatus
from .chat.private import Private
from .chat.group import Group
from .chat.channel import Channel
from .chat.history import History


class User(UserBase):
    """Class, that represented Telegram account."""

    def __init__(self, api, is_bot, first_name, **kwargs):
        """Create new API bot."""
        UserBase.__init__(self, api.new_id(api.EntityUser), is_bot, first_name, **kwargs)
        api.users[self.id] = self
        self.api = api
        self.notifications = History(self)

    def __str__(self):
        """As text."""
        return "{} (ID {})".format(self.full_name, self.id)

    @classmethod
    def from_bot(cls, api):
        """Construct User object from test bot."""
        bot = api.bot.get_me()
        return cls(
          api,
          bot.is_bot,
          bot.first_name,
          last_name=bot.last_name,
          username=bot.username,
          language_code=bot.language_code
        )

    def join(self, chat):
        """Join user to chat by invite link."""
        if self.is_bot:
            raise EmulatorException("Bot cant join to chat by invite link.")

        if chat.type == Type.Private:
            raise EmulatorException("Try join to private: {}.".format(chat))

        return chat.add_members(None, [self])

    def leave(self, chat):
        """Leave user from the chat."""
        chat_member = chat.members.get(self.id, None)
        if not chat_member:
            raise EmulatorException("Try leave from chat, with no membership.")

        if chat_member.status in [MemberStatus.Creator, MemberStatus.Left]:
            raise EmulatorException(
              "Try leave from {}, with status '{}'.".format(chat, chat_member.status)
            )

        if chat.id in self.api.bot_chats:
            chat.send(LeftChatMember(chat, self))

        if self.id == self.api.bot.id:
            self.api.bot.leave_chat(chat.id)
        else:
            del chat.members[self.id]

    def private(self):
        """Return private chat for this user. If chat not exist, create new one."""
        if self.is_bot:
            raise EmulatorException("Bot attempt to create private chat.")

        chats = self.api.chats
        if self.id in chats:
            return chats[self.id]

        chats[self.id] = Private(self)
        return chats[self.id]

    def create_group(self, title, username=None):
        """Return new group chat. Bot cant do this."""
        if self.is_bot:
            raise EmulatorException("Bot attempt to create group.")

        return Group(self, title, username=username)

    def create_channel(self, title, username=None):
        """Return new channel. Bot cant do this."""
        if self.is_bot:
            raise EmulatorException("Bot attempt to create channel.")

        return Channel(self, title, username=username)

    def stop_bot(self):
        """Remove private chat from active chat list."""
        if self.id in self.api.chats:
            del self.api.chats[self.id]

        if self.id in self.api.bot_chats:
            del self.api.bot_chats[self.id]

    def destroy(self):
        """Destroy this Telegram account."""
        self.stop_bot()
        if self.id in self.api.users:
            del self.api.users[self.id]

    def forward(self, from_chat, to_chat, message):
        """Forward message from one chat to another."""
        fwm = Text(to_chat, self, message.text)  # !!! must be Voice, Photo, etc

        fwm.forward_from = message.from_user
        fwm.forward_from_chat = from_chat
        fwm.forward_from_message_id = message.message_id
        fwm.forward_date = self.api.get_date()

        if from_chat.type == Type.Channel:
            if message.author_signature:
                fwm.forward_signature = message.author_signature

        return to_chat.send(fwm)

    def reply(self, message, text):
        """Text reply to message."""
        return message.chat.send(Text(message.chat, self, text, reply_to_message=message))
