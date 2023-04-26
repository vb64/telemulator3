"""Package for Telegram Bot API methods emulators.

Each emulator placed to separate file, that name literally equal to method name
and contain function named 'response'. This function recieve 3 arguments:

api - an ininstance of api.Telegram object
uri - the requst url string
params - set of parameters, that passed to method call

Function must return tuple of 2 items:

code - http response code
data - dictionary of data for answer
"""
import json
from ..update import markup
from .. import EmulatorException as ExceptionBase


class EmulatorException(ExceptionBase):
    """Exception with http response code and description."""

    def __init__(self, code, note):
        """Create Exception with note and code."""
        super().__init__(note)
        self.code = code
        self.note = note


def error(code, note):
    """Make error response."""
    return (
      code,
      {
        "ok": False,
        "error_code": code,
        "description": note,
      },
    )


def get_chat(api, params):
    """Extract chat from params."""
    chat_id = get_int(params, 'chat_id')
    if not chat_id:
        raise EmulatorException(400, "Wrong request: no chat_id")

    chat = api.bot_chats.get(chat_id, None)
    if not chat:
        raise EmulatorException(403, "Forbidden: bot was kicked from the chat")

    return chat


def get(params, key):
    """Return key value from params."""
    return params.get(key, None)


def get_json(params, key):
    """Return key value from params as json."""
    val = get(params, key)
    if val is None:
        return {}
    return json.loads(val)


def get_reply_markup(params):
    """Return 'reply_markup' key value from params as json."""
    return get_json(params, 'reply_markup')


def get_int(params, key):
    """Return key value from params as integer."""
    value = get(params, key)
    if value is None:
        return None

    return int(value)


def message_to_dic(message):
    """Construct sucess response for message."""
    return {
      "ok": True,
      "result": message.to_dict(),
    }


def message_for_chat(func):
    """Decorate methods, that receive chat ID and produce message in response."""
    def decorator(api, _uri, params):
        """Extract chat from params, return OK message from handler response."""
        reply_to_message_id = get_int(params, 'reply_to_message_id')
        reply_to_message = None
        reply_markup = markup.from_dict(get_reply_markup(params))

        try:
            chat = get_chat(api, params)

            if reply_to_message_id:
                try:
                    reply_to_message = chat.history.messages[reply_to_message_id]
                except KeyError as err:
                    raise EmulatorException(
                      402,
                      "Wrong reply_to_message_id: {}".format(reply_to_message_id)
                    ) from err

            message = func(api, params, chat, reply_to_message, reply_markup)

        except EmulatorException as err:
            return error(err.code, err.note)

        return (200, message_to_dic(message))

    return decorator


def with_chat(func):
    """Decorate methods, that receive chat ID and return OK response of decorated function."""
    def decorator(api, _uri, params):
        """Extract chat from params, return OK response of decorated function."""
        try:
            chat = get_chat(api, params)
        except EmulatorException as err:
            return error(err.code, err.note)

        return (200, {
          "ok": True,
          "result": func(api, params, chat),
        })

    return decorator
