"""Package for testing emulators of Telegram Bot API methods."""
from .. import TestCase


class TestMethod(TestCase):
    """Base class for testing emulators."""

    def setUp(self):
        """Init vars."""
        super().setUp()
        self.user = self.teleuser
        self.group.add_members(self.user, [self.api.get_me()])
