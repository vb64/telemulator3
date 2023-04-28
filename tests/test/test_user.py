"""Telemulator API User.

make test T=test_user.py
"""
import pytest
from . import TestCase


class TestUser(TestCase):
    """User represented Telegram account."""

    def test_private(self):
        """Test private method must return chat object for user and raise exception for bot."""
        from telemulator3 import EmulatorException

        bot = self.api.get_me()
        with pytest.raises(EmulatorException) as err:
            bot.private()
        assert "Bot attempt to create private chat" in str(err)

    def test_create_group(self):
        """Check create_group method must return new group, if user is not a bot."""
        from telemulator3 import EmulatorException

        title = "New group"
        group = self.teleuser.create_group(title)

        user2 = self.api.create_user('User2')
        user1 = self.api.create_user('User1')
        bot = self.api.get_me()

        with pytest.raises(EmulatorException) as err:
            bot.create_group(title)
        assert "Bot attempt to create group" in str(err)

        with pytest.raises(EmulatorException) as err:
            user1.leave(group)
        assert "Try leave from chat, with no membership" in str(err)

        group.add_members(self.teleuser, [bot])
        group.add_members(self.teleuser, [user1])
        user2.join(group)

        with pytest.raises(EmulatorException) as err:
            self.teleuser.leave(group)
        assert "Try leave from group" in str(err)

        assert len(group.history.messages) == 3
        assert group.history.contain('User1')
        assert group.history.contain(bot.full_name)

        user2.leave(group)
        bot.leave(group)
        user1.leave(group)

        group.add_members(self.teleuser, [user1])
        assert len(group.history.messages) == 5
        group.history.dump()  # need for coverage

    def test_create_channel(self):
        """Create_channel method must return new channel, if user is not a bot."""
        from telemulator3 import EmulatorException

        title = "New channel"
        channel = self.teleuser.create_channel(title)
        assert channel.title == title

        bot = self.api.get_me()
        with pytest.raises(EmulatorException) as err:
            bot.create_channel(title)
        assert "Bot attempt to create channel" in str(err)

        user1 = self.api.create_user('User1')
        user2 = self.api.create_user('User2')

        user1.join(channel)

        with pytest.raises(EmulatorException) as err:
            user1.join(self.teleuser.private())
        assert "Try join to private:" in str(err)

        with pytest.raises(EmulatorException) as err:
            bot.join(channel)
        assert "Bot cant join to chat by invite link" in str(err)

        with pytest.raises(EmulatorException) as err:
            channel.add_members(user2, [bot])
        assert "not a member of channel" in str(err)

        with pytest.raises(EmulatorException) as err:
            channel.add_members(user1, [bot])
        assert "does not has rights to invite new members to channel" in str(err)

        with pytest.raises(EmulatorException) as err:
            channel.add_members(self.teleuser, [bot])
        assert "Try to add bot" in str(err)

        chat_admin = channel.members[user1.id]
        chat_admin.can_invite_users = True

        with pytest.raises(EmulatorException) as err:
            channel.add_admin(user1, user2)
        assert "does not has rights to set new admins for channel" in str(err)

        with pytest.raises(EmulatorException) as err:
            channel.add_admin(None, user2)
        assert "can't join to channel" in str(err)

        chat_admin.can_promote_members = True

        channel.add_admin(user1, bot)
        channel.add_admin(user1, user2)

        assert not channel.history.messages

    def test_stop_bot(self):
        """Check stop_bot method remove private chat from active chat list."""
        self.teleuser.private()

        count1 = len(self.api.chats)
        count2 = len(self.api.bot_chats)

        self.teleuser.stop_bot()
        assert len(self.api.chats) == count1 - 1
        assert len(self.api.bot_chats) == count2 - 1
        self.teleuser.stop_bot()
        assert len(self.api.chats) == count1 - 1
        assert len(self.api.bot_chats) == count2 - 1

    def test_destroy(self):
        """Destroy method remove private chat from active chat list.

        Remove user from active user list.
        """
        old_user_count = len(self.api.users)
        self.teleuser.destroy()
        assert len(self.api.users) + 1 == old_user_count
        self.teleuser.destroy()
        assert len(self.api.users) + 1 == old_user_count

    def test_forward(self):
        """Forward message with text note from one chat to another."""
        from telemulator3.update.message import Text

        private = self.teleuser.private()
        group = self.teleuser.create_group("New group")

        src_message = group.send(Text(group, self.teleuser, "group message"))
        dst_message = self.teleuser.forward(group, private, src_message)
        assert dst_message.forward_from_message_id == src_message.message_id

        channel = self.teleuser.create_channel("New channel")
        src_message = channel.send(Text(channel, self.teleuser, "channel message"))
        dst_message = self.teleuser.forward(channel, private, src_message)
        assert dst_message.forward_from_message_id == src_message.message_id

        channel.signed_message = True
        self.teleuser.author_signature = "user sign"

        src_message = channel.send(Text(channel, self.teleuser, "channel message"))
        dst_message = self.teleuser.forward(channel, private, src_message)
        assert dst_message.forward_signature == src_message.author_signature

    def test_reply(self):
        """Check text reply to message."""
        from telemulator3.update.message import Text

        private = self.teleuser.private()
        src_message = private.send(Text(private, self.teleuser, "source message"))
        dst_message = self.teleuser.reply(src_message, "reply message")
        assert dst_message.reply_to_message.message_id == src_message.message_id
