"""Readme example.

make test T=test_readme.py
"""
from telebot import TeleBot
from telemulator3 import Telemulator, send_command

bot = TeleBot('xxx-yyy-zzz', threaded=False)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Bot answer for /start and /help."""
    bot.reply_to(message, "Howdy, how are you doing?")


# Emulate Telegram API for bot
telemul = Telemulator()
telemul.set_tested_bot(bot, username='my_bot', name='My Bot')

# At start, there are no registered users in emulated API.
assert not telemul.api.users

# Make API user, that represent our bot.
# It's a first registered user.
mybot = telemul.api.get_me()
assert mybot.is_bot
assert mybot.username == 'my_bot'
assert len(telemul.api.users) == 1

# New user open private chat with bot ond send `/start` command.
# Bot must answer as defined and his answer must be in chat history.
user = telemul.api.create_user('User')
chat = user.private()
send_command(chat, '/start', user)
assert chat.history.contain('Howdy, how are you doing?')

# User create group and add bot as member.
group = user.create_group('My group')
group.add_members(user, [mybot])
assert group.history.contain('invite new members:')

mybot.leave(group)
assert group.history.contain('My Bot (ID 1) left chat')
# group.history.dump()
