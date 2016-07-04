"""
pocha utility module
"""

class EasyDict(dict):

    def __init__(self, dictionary):
        for (key, value) in dictionary.items():
            self.__setitem__(key, value)

    def __getattr__(self, key):
        if key in self:
            return self[key]
