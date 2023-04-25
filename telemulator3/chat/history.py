"""Module for class, that represented Telegram chat history."""
from telebot.types import Chat


class History:
    """Class for Telegram chat history of messages."""

    def __init__(self, chat):
        """Create history of the chat."""
        self.messages = {}
        self.chat = chat

    def __str__(self):
        """As text."""
        return '\n'.join([self.messages[m_id] for m_id in sorted(self.messages)])

    def clear(self):
        """Clear the chat history."""
        self.messages = {}

    def dump(self, tail=5):
        """Print tail of the chat history, order by message dates."""
        suff = ''
        if len(self.messages) > tail:
            suff = 'Latest {} '.format(tail)

        if isinstance(self.chat, Chat):
            print("{}messages from {}:\n".format(suff, self.chat))
        else:
            print("{}notifications for {}:\n".format(suff, self.chat))

        for message_id in sorted(self.messages)[-tail:]:
            print(self.messages[message_id])

    def contain(self, substring, tail=5):
        """Check for presence of the substring in tail of chat history."""
        for message_id in sorted(self.messages)[-tail:]:
            if substring in str(self.messages[message_id]):
                return True

        return False
