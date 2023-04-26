"""Fubctions to convert object to dict."""
from datetime import datetime
from time import mktime
from telebot.types import Dictionaryable


def obj_to_dic(value):
    """Return dictionary for value instanse."""
    if isinstance(value, list):
        return [obj_to_dic(item) for item in value]
    if isinstance(value, datetime):
        return mktime(value.timetuple())
    if isinstance(value, Dictionaryable):
        return value.to_dict()

    return value


def attr_to_dic(obj, attr_list):
    """Return dictionary for this class instanse."""
    json_dic = {}
    for attr in attr_list:
        value = getattr(obj, attr, None)
        if value is not None:
            json_dic[attr] = obj_to_dic(value)

    return json_dic
