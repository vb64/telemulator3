"""Telegram types with specialized constructors and text representation."""
from telebot.types import (
  Message as MessageBase, MessageEntity, PhotoSize as PhotoSizeBase, Audio as AudioBase,
  Document as DocumentBase, Contact as ContactBase, Voice as VoiceBase,
  Dictionaryable,
)
from ..dictionaryable import attr_to_dic


class Message(MessageBase, Dictionaryable):
    """Base class with message_id generator."""

    def __init__(self, chat, from_user, content_type='text', **kwargs):
        """Create message."""
        chat.message_id += 1
        super().__init__(
          chat.message_id,
          from_user,
          chat.creator.api.get_date(),
          chat,
          content_type,
          kwargs,
          ''
        )
        self.buttons = None
        self.json = self.to_dict()

    def __str__(self):
        """As text."""
        user = ''
        if self.from_user:
            user = self.from_user

        reply = ''
        reply_to_message = getattr(self, 'reply_to_message', None)
        if reply_to_message:
            reply_to = self.chat.history.messages.get(
              reply_to_message.message_id,
              'MSG {}'.format(reply_to_message.message_id)
            )
            reply = 'reply to [{}] '.format(reply_to)

        return '{} >> {}'.format(user, reply)

    def to_dict(self):
        """Return dictionary for this class instanse."""
        attr_list = [
          'message_id', 'date', 'chat', 'content_type', 'forward_from', 'forward_from_chat',
          'forward_from_message_id', 'forward_signature', 'forward_date', 'reply_to_message',
          'edit_date', 'media_group_id', 'author_signature', 'text', 'entities', 'caption_entities',
          'audio', 'document', 'game', 'photo', 'sticker', 'video', 'video_note', 'voice', 'caption',
          'contact', 'location', 'venue', 'new_chat_member', 'left_chat_member', 'new_chat_title',
          'new_chat_photo', 'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created',
          'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message',
          'invoice', 'successful_payment', 'connected_website', 'new_chat_members',
        ]

        data = attr_to_dic(self, attr_list)
        if self.from_user:
            data['from'] = self.from_user.to_dict()
        if self.new_chat_members:
            data['content_type'] = 'new_chat_members'

        return data

    def dump_caption(self):
        """Return caption description for __str__ method."""
        return '' if self.caption is None else " with caption: {}".format(self.caption)

    def dump_buttons(self):
        """Return text dump of attached inline buttons."""
        if self.buttons:
            return self.buttons.dump()

        return ''


class Text(Message):
    """Text message."""

    def __init__(self, chat, from_user, text, **kwargs):
        """Create text message."""
        Message.__init__(self, chat, from_user, text=text, **kwargs)

    def __str__(self):
        """As text."""
        return '{}{}{}'.format(Message.__str__(self), self.text, self.dump_buttons())


class Command(Text):
    """Command message."""

    def __init__(self, chat, from_user, text, **kwargs):
        """Create command message."""
        entities = MessageEntity("bot_command", 0, len(text))
        Text.__init__(self, chat, from_user, text=text, entities=entities, **kwargs)


class PhotoSize(PhotoSizeBase, Dictionaryable):
    """Dictionaryable PhotoSize class."""

    def to_dict(self):
        """Return dictionary for PhotoSize instanse."""
        attr_list = ['file_id', 'file_unique_id', 'width', 'height', 'file_size']
        return attr_to_dic(self, attr_list)


class Photo(Message):
    """Photo sended to chat."""

    def __init__(
      self, chat, from_user, caption, width, height, file_size, **kwargs
    ):  # pylint: disable=too-many-arguments
        """Create photo message."""
        file_id = "photo_AD_lE2G40bZAfysKY0VU3jEWpToBkABGplqatdziomovwAAgI"
        Message.__init__(
          self, chat, from_user,
          content_type='photo',
          photo=[PhotoSize(file_id, file_id, width, height, file_size=file_size)],
          caption=caption,
          **kwargs
        )

    def __str__(self):
        """As text."""
        photo = self.photo[0]  # pylint: disable=unsubscriptable-object
        return '{}image {} bytes{}{}'.format(
          Message.__str__(self),
          photo.file_size,
          self.dump_caption(),
          self.dump_buttons()
        )


class Voice(Message):
    """Voice sended to chat."""

    def __init__(self, chat, from_user, duration, file_size, **kwargs):
        """Create voice message."""
        file_id = "voice_AD_lE2G40bZAfysKY0VU3jEWpToBkABGplqatdziomovwAAgI"
        Message.__init__(
          self, chat, from_user,
          content_type='voice',
          voice=VoiceBase(file_id, file_id, duration, mime_type='audio/ogg', file_size=file_size),
          **kwargs
        )

    def __str__(self):
        """As text."""
        return '{}voice {} bytes {} seconds{}{}'.format(
          Message.__str__(self),
          self.voice.file_size,
          self.voice.duration,
          self.dump_caption(),
          self.dump_buttons()
        )


class AudioDict(AudioBase, Dictionaryable):
    """Dictionaryable AudioBase class."""

    def to_dict(self):
        """Return dictionary for Audio instanse."""
        attr_list = [
          'file_id', 'file_unique_id', 'duration', 'performer', 'title',
          'file_name', 'mime_type', 'file_size', 'thumbnail',
        ]
        return attr_to_dic(self, attr_list)


class Audio(Message):
    """Audio sended to chat."""

    def __init__(
      self, chat, from_user, duration, file_size, performer, title, **kwargs
    ):  # pylint: disable=too-many-arguments
        """Create audio message."""
        file_id = "audio_AD_lE2G40bZAfysKY0VU3jEWpToBkABGplqatdziomovwAAgI"
        Message.__init__(
          self, chat, from_user,
          content_type='audio',
          audio=AudioDict(
            file_id, file_id, duration,
            performer=performer, title=title, mime_type='audio/mp3', file_size=file_size
          ),
          **kwargs
        )

    def __str__(self):
        """As text."""
        return '{}audio {} bytes {} seconds{}{}'.format(
          Message.__str__(self),
          self.audio.file_size,
          self.audio.duration,
          self.dump_caption(),
          self.dump_buttons()
        )


class DocumentDict(DocumentBase, Dictionaryable):
    """Dictionaryable DocumentBase class."""

    def to_dict(self):
        """Return dictionary for Audio instanse."""
        attr_list = [
          'file_id', 'file_unique_id', 'thumbnail', 'file_name',
          'mime_type', 'file_size',
        ]
        return attr_to_dic(self, attr_list)


class Document(Message):
    """Document sended to chat."""

    def __init__(self, chat, from_user, file_name, file_size, **kwargs):
        """Create document message."""
        file_id = "document_E2G40bZAfysKY0VU3jEWpToBkABGplqatdziomovwAAgI"
        doc = DocumentDict(
          file_id, file_id,
          thumb=None,
          file_name=file_name,
          mime_type='application/json',
          file_size=file_size
        )
        Message.__init__(self, chat, from_user, content_type='document', document=doc, **kwargs)

    def __str__(self):
        """As text."""
        return '{}document {} ({} bytes){}{}'.format(
          Message.__str__(self),
          self.document.file_name,
          self.document.file_size,
          self.dump_caption(),
          self.dump_buttons()
        )


class Contact(Message):
    """Contact of the user sended to chat."""

    def __init__(
      self, chat, from_user, phone_number, first_name, last_name, user_id, **kwargs
    ):  # pylint: disable=too-many-arguments
        """Create contact message."""
        contact = ContactBase(
          phone_number,
          first_name,
          last_name=last_name,
          user_id=user_id,
          **kwargs
        )
        Message.__init__(self, chat, from_user, content_type='contact', contact=contact, **kwargs)

    def __str__(self):
        """As text."""
        return '{}contact {}{}'.format(
          Message.__str__(self), self.contact.phone_number, self.dump_buttons()
        )


class NewChatMembers(Message):
    """New chat members invited to chat by from_user.

    If from_user is None, then members join to chat by invite link.
    """

    def __init__(self, chat, from_user, members):
        """Create new chat member message."""
        Message.__init__(self, chat, from_user, content_type='new_chat_members', new_chat_members=members)

    def __str__(self):
        """As text."""
        users = ', '.join(
          ["'{}'".format(user) for user in self.new_chat_members]  # pylint: disable=not-an-iterable
        )

        if self.from_user:
            line = 'invite new members: {}'.format(users)
        else:
            line = 'joined by invite link: {}'.format(users)

        return '{}{}'.format(Message.__str__(self), line)


class LeftChatMember(Message):
    """User left the chat."""

    def __init__(self, chat, left_user):
        """Create left chat member message."""
        Message.__init__(self, chat, None, content_type='left_chat_member', left_chat_member=left_user)

    def __str__(self):
        """As text."""
        return '{}{} left chat'.format(Message.__str__(self), self.left_chat_member)
