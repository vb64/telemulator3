"""Telemulator properties.

make test T=test_init.py
"""
import os
from . import TestCase


class TestInit(TestCase):
    """Telemulator properties."""

    def test_bot(self):
        """Bot properties."""
        assert self.telemul
        assert self.telemul.bot
        assert self.telemul.bot.name == 'Test bot'
        assert self.telemul.bot.username == 'bot-username'
        assert self.telemul.bot.token == 'xxx-yyy-zzz'

    def test_clean_proxy(self):
        """Bot clean_proxy method."""
        os.environ['http_proxy'] = 'xxx'
        assert 'http_proxy' in os.environ
        self.telemul.clean_proxy()
        assert 'http_proxy' not in os.environ

    def test_create_group(self):
        """Check create_group call."""
        group = self.telemul.create_group("Test group", self.teleuser)
        assert len(group.members) == 1
        assert self.teleuser.id in group.members
        assert group.members[self.teleuser.id].can_invite_users

        bot = self.api.get_me()
        group = self.telemul.create_group("Test group", self.teleuser, members=[bot])
        assert len(group.members) == 2
        assert self.teleuser.id in group.members
        assert bot.id in group.members

        user = self.api.create_user('New User')
        group = self.telemul.create_group("Test group", user, members=[bot])
        assert len(group.members) == 2
        assert user.id in group.members
        assert bot.id in group.members
        assert self.teleuser.id not in group.members

    def test_create_channel(self):
        """Test create_channel call."""
        channel = self.telemul.create_channel("Test channel", self.teleuser, add_bot=False)
        assert len(channel.members) == 1

        user = self.api.create_user('New User')
        channel = self.telemul.create_channel("Test channel", user)
        assert len(channel.members) == 2
