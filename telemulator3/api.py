"""Telegram messenger Bot API emulator."""
import os
import re
from io import BytesIO
import cgi
import json
import importlib
from time import mktime
from datetime import datetime
import httpretty
# from telebot.types import Update as TeleUpdate

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


def emulate_bot(api, http_method):
    """Return decorator that emulate Telegram Bot API call."""
    def decorator(request, uri, headers):
        """Return code and body of answer to Telegram Bot API call."""
        params = request.querystring
        # https://httpretty.readthedocs.io/en/latest/api.html
        # https://stackoverflow.com/questions/25645253/python-parsing-multipart-form-data-request-on-server-side
        # https://stackoverflow.com/questions/34326150/multipartparsererror-invalid-boundary
        # https://www.programcreek.com/python/example/6138/cgi.parse_multipart
        if http_method == 'POST':
            params = request.parsed_body
            if 'boundary=' in request.headers.get('Content-Type', ''):
                _ctype, pdict = cgi.parse_header(request.headers['Content-Type'])
                params = cgi.parse_multipart(
                  BytesIO(request.body.encode('utf-8')),
                  {i: j.encode('utf-8') for i, j in pdict.items()}
                )

            for key in params:
                if key in ['text', 'reply_markup']:
                    params[key] = fix_ampersand(params[key])

        if DEBUG_PRINT:
            print("#{} -> {}".format(http_method, uri))
            print("#params -> {}".format(params))

        method_name = uri[uri.index(api.bot.token) + len(api.bot.token) + 1:]
        tmp = method_name.find('?')
        if tmp > 0:
            method_name = method_name[:tmp]

        code, data = api.get_answer(method_name, uri, params)
        return (code, headers, json.dumps(data))

    return decorator


def emulate_file(api, http_method):
    """Return decorator that emulate Telegram File API call."""
    def decorator(request, uri, headers):
        """Return code and body of file to Telegram File API call."""
        if DEBUG_PRINT:
            print("#{} -> {}".format(http_method, uri))

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

        url_bot = re.compile('https://api.telegram.org/bot.*')
        url_file = re.compile('https://api.telegram.org/file/bot.*')

        for method in [httpretty.GET, httpretty.POST]:
            httpretty.register_uri(method, url_bot, body=emulate_bot(self, method))
            httpretty.register_uri(method, url_file, body=emulate_file(self, method))

    def get_answer(self, method_name, uri, params):
        """Return response code and answer for request by method_name."""
        if method_name in self.answers:
            code, data = self.answers[method_name]
            return (code, data)

        try:
            method = importlib.import_module(PACKAGE_PREFIX + ".method." + method_name)
            code, data = method.response(self, uri, params)
        except ImportError:
            code = 400
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

    @staticmethod
    def emulate_start():
        """Trap calls to Telegram."""
        httpretty.enable()

    @staticmethod
    def emulate_stop():
        """Don't trap calls to Telegram."""
        httpretty.disable()

    def get_me(self):
        """Create and put to active users list instanse of the tested bot."""
        if not self._me:
            self._me = User.from_bot(self)
            self.bot.id = self._me.id

        return self._me
