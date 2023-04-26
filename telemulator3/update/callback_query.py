"""CallbackQuery module."""
from telebot.types import CallbackQuery as CallbackQueryBase


class CallbackQuery(CallbackQueryBase):
    """Construct and return CallbackQuery."""

    def __init__(self, from_user, callback_data, chat_instance, message):
        """Create callback from user."""
        api = from_user.api
        callback_id = api.new_id(api.EntityCallback)
        CallbackQueryBase.__init__(self, callback_id, from_user, callback_data, chat_instance, message)
        from_user.api.callback_queries[callback_id] = self

    def __str__(self):
        """As text."""
        return '{} >> tap inline button with callback_data: {}'.format(self.from_user, self.data)
