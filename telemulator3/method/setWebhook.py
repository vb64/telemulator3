"""Module for setWebhook method emulator."""


def response(_api, _uri, _params):
    """Return data of registered webhook."""
    # print "#setWebhook uri", uri
    # print "#setWebhook params", _params
    data = {
      "ok": True,
      "result": True,
      "description": "Webhook is already set",
    }
    return (200, data)
