"""Telegram messenger Bot API emulator."""
# import os
# import re
# import json
# import importlib
# from time import mktime
# from datetime import datetime
# import httpretty
# from telebot.types import Update as TeleUpdate


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
        """API instance."""
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
