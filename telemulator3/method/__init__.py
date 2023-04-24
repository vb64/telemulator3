"""Package for Telegram Bot API methods emulators.

Each emulator placed to separate file, that name literally equal to method name
and contain function named 'response'. This function recieve 3 arguments:

api - an ininstance of api.Telegram object
uri - the requst url string
params - set of parameters, that passed to method call

Function must return tuple of 2 items:

code - http response code
data - dictionary of data for answer
"""
