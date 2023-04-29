# Library telemulator3

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vb64/telemulator3/pep257.yml?label=Pep257&style=plastic&branch=main)](https://github.com/vb64/telemulator3/actions?query=workflow%3Apep257)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vb64/telemulator3/py3.yml?label=Python%203.7-3.11&style=plastic&branch=main)](https://github.com/vb64/telemulator3/actions?query=workflow%3Apy3)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/fe568012ee1649b89bafbb4de163a0c0)](https://app.codacy.com/gh/vb64/telemulator3/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/fe568012ee1649b89bafbb4de163a0c0)](https://app.codacy.com/gh/vb64/telemulator3/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)

The free, open-source telemulator3 library designed to simplify automatic testing of Telegram bots created using the [pyTelegramBotAPI library](https://github.com/eternnoir/pyTelegramBotAPI).

The telemulator3 library partially emulates the Telegram Bot API in unit tests and allows you to create typical scenarios for the interaction of your bot with the Telegram Bot API.

## Installation

```bash
pip install telemulator3
```

## Usage

Create TeleBot instance and start emulate Telegram API for bot.

```python
from telebot import TeleBot
from telemulator3 import Telemulator, send_command

bot = TeleBot('xxx-yyy-zzz', threaded=False)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Bot answer for /start and /help."""
    bot.reply_to(message, "Howdy, how are you doing?")

telemul = Telemulator()
telemul.set_tested_bot(bot, username='my_bot', name='My Bot')
```

At start, there are no registered users in emulated API.

```python
assert not telemul.api.users
```

Make API user, that represent our bot.
It's a first registered user.

```python
mybot = telemul.api.get_me()
assert mybot.is_bot
assert mybot.username == 'my_bot'
assert len(telemul.api.users) == 1
```

New user open private chat with bot ond send `/start` command.
Bot must answer as defined and his answer must be in chat history.

```python
user = telemul.api.create_user('User')
chat = user.private()
send_command(chat, '/start', user)
assert chat.history.contain('Howdy, how are you doing?')
```

User create group and add bot as member.

```python
group = user.create_group('My group')
group.add_members(user, [mybot])
assert group.history.contain('invite new members:')
```

And so on.

```python
mybot.leave(group)
assert group.history.contain('My Bot (ID 1) left chat')
# group.history.dump()
```

## Development

```
$ git clone git@github.com:vb64/telemulator3
$ cd telemulator3
$ make setup PYTHON_BIN=/path/to/python3
$ make tests
```
