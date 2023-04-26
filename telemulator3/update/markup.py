"""Markup factory module."""
from telebot.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, JsonDeserializable
from .. import EmulatorException  # pylint: disable=cyclic-import
from .callback_query import CallbackQuery


def from_dict(data_dict):
    """Detect markup type for passed dictionary and call apropriate constructor."""
    if not data_dict:
        return None
    keyboard_types = {
      'keyboard': KeyboardMarkup,
      'remove_keyboard': KeyboardRemove,
      'inline_keyboard': InlineKeyboard,
    }
    for item, cls in keyboard_types.items():
        if item in data_dict:
            return cls.de_json(data_dict)

    raise EmulatorException("Unknown markup type: '{}'.".format(data_dict))


def dump_inline_button(button_dict):
    """Return text representation for types.InlineKeyboardButton dict."""
    button_types = [
      'url', 'pay', 'callback_data', 'callback_game',
      'switch_inline_query', 'switch_inline_query_current_chat',
    ]

    for item in button_types:
        if item in button_dict:
            return "\n[{}]({}: {})".format(button_dict['text'], item, button_dict[item])

    raise EmulatorException(
      "Unknown inline button markup type: {}".format(button_dict)
    )


class InlineKeyboard(InlineKeyboardMarkup):
    """Construct and return types.InlineKeyboardMarkup from the given dictionary."""

    def __init__(self):
        """Create inline keyboard."""
        InlineKeyboardMarkup.__init__(self)
        self.parent_message = None

    @classmethod
    def de_json(cls, json_string):
        """Convert from json to class instanse."""
        obj = cls.check_json(json_string)
        cls_obj = cls()
        cls_obj.keyboard = obj.get('inline_keyboard', [])

        return cls_obj

    def attach(self, message):
        """Attach this inline keyboard to message instanse."""
        self.parent_message = message
        self.parent_message.buttons = self

    def dump(self):
        """Return text dump of attached inline buttons."""
        ret = "\n----------"
        for row in self.keyboard:
            for col in row:
                ret += dump_inline_button(col)

        return ret

    def tap(self, from_user, col, row=0):
        """User tap inline button."""
        button = self.keyboard[row][col].to_dict()

        if 'url' in button:
            if self.parent_message:
                from . message import Text
                return self.parent_message.chat.send(
                  Text(self.parent_message.chat, from_user, "Goto to url: {}".format(button['url']))
                )

        elif 'callback_data' in button:
            chat, message_id = None, None
            if self.parent_message:
                chat = self.parent_message.chat

            chat_instance = from_user.id
            if chat:
                chat_instance = chat.id
                chat.message_id += 1
                message_id = chat.message_id

            callback_query = CallbackQuery(
              from_user,
              button['callback_data'],
              str(chat_instance),
              message=self.parent_message
            )

            from_user.api.send_update(
              chat,
              from_user,
              (message_id, callback_query),
              callback_query=callback_query
            )

            return callback_query

        else:
            raise EmulatorException(
              "Unknown inline button type: {}".format(button)
            )

        return None


class KeyboardMarkup(ReplyKeyboardMarkup, JsonDeserializable):
    """Construct and return types.ReplyKeyboardMarkup from the given dictionary."""

    keyboard = None

    @classmethod
    def de_json(cls, json_string):
        """From json."""
        obj = cls.check_json(json_string)
        kwargs = {
          item: obj.get(item, None) for item in [
            'selective',
            'resize_keyboard',
            'one_time_keyboard',
          ]
        }

        cls_obj = cls(**kwargs)
        cls_obj.keyboard = obj.get('keyboard', [])

        return cls_obj


class KeyboardRemove(ReplyKeyboardRemove, JsonDeserializable):
    """Construct and return types.ReplyKeyboardRemove from the given dictionary."""

    @classmethod
    def de_json(cls, json_string):
        """From json."""
        obj = cls.check_json(json_string)
        selective = obj.get('selective', None)

        return cls(selective=selective)
