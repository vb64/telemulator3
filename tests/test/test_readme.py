"""Readme example.

make test T=test_readme.py
"""
import unittest
from telebot import TeleBot
from telemulator3 import Telemulator, send_command


class TestCase(unittest.TestCase, Telemulator):
    """Testing with Telemulator."""

    def setUp(self):
        """Connect your bot to test suite."""
        super().setUp()
        self.set_tested_bot(TeleBot('xxx-yyy-zzz', threaded=False))

        # Your bot is available via api property.
        # Your need to set bot name and username.
        self.api.bot.username = 'my_bot'
        self.api.bot.name = 'My Bot'

    def test_api(self):
        """Play with API calls."""
        assert not self.api.users

        # create API user for our bot
        bot = self.api.get_me()
        assert bot.is_bot
        assert bot.username == 'my_bot'

        # our bot is a first registered user
        assert len(self.api.users) == 1

        # new user open private chat with bot
        user = self.api.create_user('User')
        chat = user.private()
        send_command(chat, '/start', user)
        assert chat.history.contain('/start')

        # user create group and add bot as member
        group = user.create_group('My group')
        group.add_members(user, [bot])
        assert group.history.contain('invite new members:')

        bot.leave(group)
        assert group.history.contain('My Bot (ID 1) left chat')
        # group.history.dump()
