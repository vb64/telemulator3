"""Fubctions to convert object to dict."""
from datetime import datetime
from time import mktime
from telebot.types import Dictionaryable as DictionaryableBase


def obj_to_dic(value):
    """Return dictionary for value instanse."""
    if isinstance(value, list):
        return [obj_to_dic(item) for item in value]
    if isinstance(value, datetime):
        return mktime(value.timetuple())
    if isinstance(value, (Dictionaryable, DictionaryableBase)):
        return value.to_dict()

    return value


class Dictionaryable:
    """Subclasses of this class are guaranteed to be able to be converted to dictionary.

    All subclasses of this class must must define attr_list property with field names list,
    that will be included in dictionary by to_dict() method call.
    """

    attr_list = []

    def to_dict(self):
        """Return a DICT with class field values from attr_list property."""
        json_dic = {}
        for attr in self.attr_list:
            value = getattr(self, attr, None)
            if value is not None:
                json_dic[attr] = obj_to_dic(value)

        return json_dic
