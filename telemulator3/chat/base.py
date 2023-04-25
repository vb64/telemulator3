"""Module for base class of all Telegram chats."""
from telebot.types import Chat as ChatBase
from .. import EmulatorException  # pylint: disable=cyclic-import

from . import Type
from .history import History
from .keyboard import Keyboard


class Chat(ChatBase):
    """Class, that represented common object of Telegram chat."""

    def __init__(self, creator, chat_type, start_message_id=0, **kwargs):
        """Create new chat."""
        self.creator = creator
        if chat_type == Type.Private:
            chat_id = self.creator.id
        else:
            self.creator.api.ids['chat'] += 1
            chat_id = self.creator.api.ids['chat']

        super().__init__(self, chat_id, chat_type, **kwargs)
        self.message_id = start_message_id
        self.history = History(self)
        self.members = {}
        self.keyboard = Keyboard(self)
        self.creator.api.chats[chat_id] = self
        self.signed_message = False

    def __str__(self):
        """As text."""
        return "{} '{}'".format(self.type, self.title)

    def check_can_write(self, user):
        """Raise exception in user not chat member."""
        if user and (user.id not in self.members):
            raise EmulatorException(
              "User '{}' is not member of {} and try to send message here.".format(user, self)
            )

    def send(self, message, reply_markup=None):
        """Send message to Telegram API."""
        self.check_can_write(message.from_user)
        self.keyboard.assign(message, reply_markup)

        if self.type == Type.Channel:

            if self.signed_message:
                message.author_signature = str(message.from_user)

            self.creator.api.send_update(
              self,
              message.from_user,
              (message.message_id, message),
              channel_post=message
            )

        else:
            self.creator.api.send_update(
              self,
              message.from_user,
              (message.message_id, message),
              message=message
            )

        return message

    def check_add_members_rigts(self, admin, members):
        """Check for add new chat members case."""
        if admin:
            if admin.id not in self.members:
                raise EmulatorException(
                  "User '{}' not a member of {}.".format(admin, self)
                )

            if not self.members[admin.id].can_invite_users:
                raise EmulatorException(
                  "User '{}' does not has rights to invite new members to {}.".format(admin, self)
                )

        if not members:
            raise EmulatorException(
              "User '{}' try to add empty member list to {}.".format(admin, self)
            )
