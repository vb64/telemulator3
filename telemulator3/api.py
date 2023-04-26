"""Telegram messenger Bot API emulator."""
import os
import importlib
from time import mktime
from datetime import datetime
from telebot.types import Update as TeleUpdate

from .user import User

DEBUG_PRINT = False
HTTPRETTY_AMPERSAND = '_httpretty_amp_'
PACKAGE_PREFIX = os.path.basename(os.path.dirname(os.path.abspath(__file__)))


def debug_print(is_on):
    """Switch printing calls to Telegram API."""
    global DEBUG_PRINT  # pylint: disable=global-statement
    DEBUG_PRINT = is_on


def fix_ampersand(text_list):
    """Replace apihelper.HTTPRETTY_AMPERSAND with '&' in each string in list."""
    return [i.replace(HTTPRETTY_AMPERSAND, '&') for i in text_list]


class Result:
    """Valid object for telebot.apihelper._check_result call."""

    def __init__(self, code, data):
        """Create with eercode and data.

        If data['ok'] == False, data must contain keys: 'error_code', 'description'.
        """
        self.status_code = code
        self.data = data
        self.reason = 'Test reason'
        self.text = 'Test description'

    def json(self):
        """Return data."""
        return self.data


def emulate_bot(api):
    """Return handler that emulate telebot.apihelper._make_request call."""
    def custom_request_sender(method, uri, params=None, files=None, timeout=None, proxies=None):
        """Return object valid for telebot.apihelper._check_result call."""
        if DEBUG_PRINT:
            print("#{} -> {} timeout {} proxies {}".format(method, uri, timeout, proxies))
            print("#params -> {}".format(params))
            print("#files -> {}".format(files))

        method_name = uri[uri.index(api.bot.token) + len(api.bot.token) + 1:]
        tmp = method_name.find('?')
        if tmp > 0:
            method_name = method_name[:tmp]

        code, data = api.get_answer(method_name, uri, params, files)
        return Result(code, data)

    return custom_request_sender


def emulate_file(api):
    """Return decorator that emulate Telegram File API call."""
    def decorator(request, uri, headers):
        """Return code and body of file to Telegram File API call."""
        if DEBUG_PRINT:
            print("#{} -> {}".format('file', uri))

        # print "##", request.path, request.body
        file_name = request.path.split('/')[-1]
        code, data = api.get_file(file_name)

        return (code, headers, data)

    return decorator


class Telegram:
    """This class represents an Telegram Bot API for pyTelegramBotAPI Telebot instance.

    Parameters start_user_id and start_chat id must be significantly differs,
    because private chats has same id as users and saved in one dictionary with other chat id's
    """

    def __init__(  # pylint: disable=too-many-arguments
      self,
      bot,
      file_store_path=None,
      start_update_id=0,
      start_callback_query_id=0,
      start_user_id=0,
      start_chat_id=1000,
    ):
        """Create API instance."""
        self.custom_date = None
        self.custom_file_content = None
        self.file_store_path = file_store_path

        self.bot = bot
        self.bot.id = 0
        self._me = None

        self.users = {}
        self.chats = {}
        self.callback_queries = {}
        self.ids = {
          'update': start_update_id,
          'user': start_user_id,
          'chat': start_chat_id,
          'callback_query': start_callback_query_id,
        }
        self.answers = {}
        self.bot_chats = {}

        from telebot import apihelper
        apihelper.CUSTOM_REQUEST_SENDER = emulate_bot(self)

    def get_answer(self, method_name, uri, params, _files):
        """Return response code and answer for request by method_name."""
        if method_name in self.answers:
            code, data = self.answers[method_name]
            return (code, data)

        try:
            method = importlib.import_module(PACKAGE_PREFIX + ".method." + method_name)
            code, data = method.response(self, uri, params)
        except ImportError:
            code = 200
            data = {
              "ok": False,
              "error_code": 400,
              "description": "Wrong method name: {}".format(method_name),
            }

        return (code, data)

    def get_file(self, file_name):
        """Return response code and content for file file_name."""
        if self.custom_file_content:
            return (200, self.custom_file_content)

        if self.file_store_path:
            try:
                return (200, open(os.path.join(self.file_store_path, file_name), 'rb').read())
            except IOError as err:
                return (400, str(err))

        return (200, "file content stub")

    def get_date(self):
        """Return current or emulated date."""
        if self.custom_date:
            return self.custom_date

        return datetime.utcnow()

    def get_date_int(self):
        """Return current or emulated date as unix time (integer)."""
        return mktime(self.get_date().timetuple())

    def get_me(self):
        """Create and put to active users list instanse of the tested bot."""
        if not self._me:
            self._me = User.from_bot(self)
            self.bot.id = self._me.id

        return self._me

    def send_update(  # pylint: disable=too-many-arguments,too-many-locals
      self, chat, from_user, history_item,
      message=None, edited_message=None, channel_post=None, edited_channel_post=None,
      inline_query=None, chosen_inline_result=None, callback_query=None,
      shipping_query=None, pre_checkout_query=None, poll=None, poll_answer=None,
      my_chat_member=None, chat_member=None, chat_join_request=None,
    ):
        """Create Update object and pass it to bot for processing.

        Put update description, that passed in history_item parameter to appropriate chat history.
        """
        self.ids['update'] += 1

        if chat:
            item_id, item_body = history_item
            chat.history.messages[item_id] = item_body

        if callback_query:
            self.callback_queries[callback_query.id] = callback_query

        # filter out messages from tested bot
        if from_user and (from_user.id == self.get_me().id):
            return None

        update = TeleUpdate(
          self.ids['update'],
          message, edited_message, channel_post, edited_channel_post, inline_query,
          chosen_inline_result, callback_query, shipping_query, pre_checkout_query,
          poll, poll_answer, my_chat_member, chat_member, chat_join_request
        )
        self.bot.process_new_updates([update])

        return update

    def create_user(self, first_name, last_name=None, username=None, language_code=None):
        """Create new Telegram account."""
        return User(
          self,
          False,
          first_name,
          last_name=last_name,
          username=username,
          language_code=language_code
        )

    def create_bot(self, first_name, username):
        """Create new Telegram bot."""
        return User(
          self,
          True,
          first_name,
          last_name=None,
          username=username,
          language_code=None
        )
