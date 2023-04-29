"""Telemulator properties.

make test T=test_init.py
"""
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

    def test_call_query(self):
        """Check call_query."""
        assert self.telemul.call_query(self.teleuser, 'xxx-yyy', self.tele_message)

    def test_tap_inline_button(self):
        """Check tap_inline_button."""
        assert self.telemul.tap_inline_button(self.teleuser, self.tele_message, 'xxx-yyy')

    def test_helpers(self):
        """Check send_* and private_* helper functions."""
        from telemulator3 import (
          private_command, private_text, private_document, private_photo, private_voice, private_contact,
        )

        user = self.teleuser

        assert private_command("/start", user)
        assert private_text("hi!", user)
        assert private_document("test.txt", user)
        assert private_photo(user)
        assert private_voice(user)
        assert private_contact("212-85-06", user, first_name="My", last_name="Contact", user_id="xxx-zzz")
