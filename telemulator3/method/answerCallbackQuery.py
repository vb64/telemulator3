# pylint: disable=invalid-name
"""Module for answerCallbackQuery method emulator."""
from . import get_int, get, error


def response(api, _uri, params):
    """Notify origin user of callback query."""
    # print "#answerCallbackQuery uri", uri
    # print "#answerCallbackQuery params", params
    callback_query_id = get_int(params, 'callback_query_id')
    if callback_query_id not in api.callback_queries:
        return error(400, "Wrong callback_query_id: {}".format(params))

    text = get(params, 'text')
    if text:
        callback_query = api.callback_queries[callback_query_id]
        if callback_query.from_user:
            callback_query.from_user.notifications.messages[callback_query_id] = text

    data = {
      "ok": True,
      "result": True
    }

    return (200, data)
