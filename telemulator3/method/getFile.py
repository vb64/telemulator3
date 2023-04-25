# pylint: disable=invalid-name
"""Module for getFile method emulator."""


def response(_api, _uri, _params):
    """Return data for passed file_id."""
    # print "#getFile uri", uri
    # print "#getFile params", _params
    data = {
      "ok": True,
      "result": {
        "file_id": "AgADAgADsacxG0gMnggDmmEhKp-RHSoNSw0ABIjmXO6ouSWqwVIAAgI",
        "file_size": 500,
        "file_path": "file_3.jpg",
      },
    }
    return (200, data)
