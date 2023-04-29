"""Readme example.

make test T=test_readme.py
"""
from telebot import TeleBot
from telemulator3 import Telemulator, send_command

bot = TeleBot('xxx-yyy-zzz', threaded=False)


# @bot.message_handler(commands=['start', 'help'])
# def send_welcome(message):
# 	bot.reply_to(message, "Howdy, how are you doing?")

telemul = Telemulator()

# Start emulation for bot
telemul.set_tested_bot(bot)

# Your bot is available via api property.
# Your need to set bot name and username.
telemul.api.bot.username = 'my_bot'
telemul.api.bot.name = 'My Bot'

# Play with API calls.
assert not telemul.api.users

# create API user for our bot
bot = telemul.api.get_me()
assert bot.is_bot
assert bot.username == 'my_bot'

# our bot is a first registered user
assert len(telemul.api.users) == 1

# new user open private chat with bot
user = telemul.api.create_user('User')
chat = user.private()

# print('###')
# telemul.print_trace(True)

send_command(chat, '/start', user)
assert chat.history.contain('/start')
chat.history.dump()

# user create group and add bot as member
group = user.create_group('My group')
group.add_members(user, [bot])
assert group.history.contain('invite new members:')

bot.leave(group)
assert group.history.contain('My Bot (ID 1) left chat')
# group.history.dump()
