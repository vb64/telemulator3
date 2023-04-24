# pylint: disable=invalid-name
"""Module for getMe method emulator."""


def response(api, _uri, _params):
    """Return data of registered in api test bot.

    Cant use api.get_me().to_dic() because it run infinite loop.
    """
    # print "#getMe uri", uri
    # print "#getMe params", params
    data = {
      "ok": True,
      "result": {
        "id": api.bot.id,
        "is_bot": True,
        "first_name": api.bot.name,
        "username": api.bot.username,
      }
    }
    return (200, data)
