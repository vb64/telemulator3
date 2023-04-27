"""Telemulator API Message update class.

make test T=test_update/test_message.py
"""
from . import TestUpdate


class TestMessage(TestUpdate):
    """Tests for Telegram messages of various types."""

    def test_message(self):
        """Test message."""
        from telemulator3.update.message import Message

        msg = Message(self.private, None)
        assert str(msg) == ' >> '

    def test_common(self):
        """Test common messages."""
        from telemulator3.update.message import Text, NewChatMembers

        message = Text(self.private, self.teleuser, "Hello!")
        data = message.to_dict()
        assert data['text'] == "Hello!"

        group = self.teleuser.create_group("Test group")
        message = NewChatMembers(group, self.teleuser, [self.api.get_me()])
        data = message.to_dict()
        assert data['new_chat_members'][0]['is_bot'] is True

    def test_command(self):
        """Test Command message."""
        from telemulator3.update.message import Command

        message = Command(self.private, self.teleuser, "/start")
        assert message.entities.type == 'bot_command'

    def test_photo(self):
        """Test Photo message."""
        from telemulator3.update.message import Photo

        message = Photo(self.private, self.teleuser, 'my image', 100, 100, 200)
        assert "image 200 bytes with caption: my image" in str(message)

    def test_voice(self):
        """Test Voice message."""
        from telemulator3.update.message import Voice

        message = Voice(self.private, self.teleuser, 10, 200)
        assert "voice 200 bytes 10 seconds" in str(message)

    def test_audio(self):
        """Test Audio message."""
        from telemulator3.update.message import Audio

        message = Audio(self.private, self.teleuser, 100, 2000, 'performer', 'mp3 title')
        assert "audio 2000 bytes 100 seconds" in str(message)

    def test_document(self):
        """Test Document message."""
        from telemulator3.update.message import Document

        message = Document(self.private, self.teleuser, 'my_file.txt', 200)
        assert "document my_file.txt (200 bytes)" in str(message)

    def test_contact(self):
        """Test Contact message."""
        from telemulator3.update.message import Contact

        message = Contact(self.private, self.teleuser, '2128506', 'Xxx', 'Yyy', None)
        assert "contact 2128506" in str(message)
