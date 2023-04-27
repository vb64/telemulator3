"""Chat history.

make test T=test_chat/test_history.py
"""
from . import TestChat


class TestHistory(TestChat):
    """Test chat history."""

    def test_default(self):
        """Test Histoty class of the chat."""
        from telemulator3.chat.history import History

        private = self.teleuser.private()
        history = History(private)
        history.messages[999] = 'test message1'
        history.dump()
        assert history.contain("message1")
        assert not history.contain("message2")

        history.messages[1] = 'test message2'
        history.messages[2] = 'test message3'
        history.dump(tail=2)

        assert 'test message3' in str(history)
