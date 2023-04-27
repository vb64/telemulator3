"""Private chat.

make test T=test_chat/test_private.py
"""
import pytest
from . import TestChat


class TestPrivate(TestChat):
    """Test private chat."""

    def test_duplicate(self):
        """Test try to create duplicate private chat."""
        from telemulator3 import EmulatorException
        from telemulator3.chat.private import Private

        self.teleuser.private()
        with pytest.raises(EmulatorException) as err:
            Private(self.teleuser)
        assert "Try to create existing private:" in str(err)

    def test_add_members(self):
        """Check for add_members method must raise exception if call for private chat."""
        from telemulator3 import EmulatorException

        private = self.teleuser.private()
        bot = self.api.create_bot('Test', 'test_bot')

        with pytest.raises(EmulatorException) as err:
            private.add_members(self.teleuser, [bot])
        assert "Attempt to add members to the private chat:" in str(err)
