"""Module for class, that represented Telegram chat member."""
from telebot.types import ChatMember as ChatMemberBase


class ChatMember(ChatMemberBase):
    """Telegram chat member class."""

    def __init__(  # pylint: disable=too-many-arguments,too-many-locals
      self,
      user,
      status,

      # Administrators only.
      #
      # channels only
      # True, if the administrator can post in the channel
      can_post_messages=False,
      # True, if the administrator can edit messages of other users and can pin messages
      can_edit_messages=False,

      # supergroups only
      # True, if the administrator can pin messages
      can_pin_messages=False,

      # True, if the bot is allowed to edit administrator privileges of that user
      can_be_edited=False,
      # True, if the administrator can change the chat title, photo and other settings
      can_change_info=False,
      # True, if the administrator can delete messages of other users
      can_delete_messages=False,
      # True, if the administrator can invite new users to the chat
      can_invite_users=False,
      # True, if the administrator can restrict, ban or unban chat members
      can_restrict_members=False,
      # True, if the administrator can add new administrators with a subset
      # of his own privileges or demote administrators that he has promoted, directly or indirectly
      # (promoted by administrators that were appointed by the user)
      can_promote_members=False,

      # Restricted and kicked only.
      #
      # Date when restrictions will be lifted for this user, unix time
      until_date=0,

      # Restricted only.
      #
      # True, if the user can send text messages, contacts, locations and venues
      can_send_messages=False,
      # True, if the user can send audios, documents, photos, videos, video notes
      # and voice notes, implies can_send_messages
      can_send_media_messages=False,
      # True, if the user can send animations, games, stickers and use inline bots,
      # implies can_send_media_messages
      can_send_other_messages=False,
      # True, if user may add web page previews to his messages,
      # implies can_send_media_messages
      can_add_web_page_previews=False
    ):
        """Create chat member with given rights."""
        ChatMemberBase.__init__(
          self,
          user,
          status,
          until_date,
          can_be_edited,
          can_change_info,
          can_post_messages,
          can_edit_messages,
          can_delete_messages,
          can_invite_users,
          can_restrict_members,
          can_pin_messages,
          can_promote_members,
          can_send_messages,
          can_send_media_messages,
          can_send_other_messages,
          can_add_web_page_previews
        )
