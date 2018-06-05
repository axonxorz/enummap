"""
Provide an enumerated type for Python.

Easy declarations mapping keys to values. Provides dict-like access on the
enum class to retrieve a value mapping
"""

from types import TupleType

__version__ = '0.1.1'
__author_name__ = 'Brendan Zerr'
__author_email__ = 'bzerr@brainwire.ca'
__license__ = 'BSD'
__url__ = 'None'

class EnumMapMeta(type):
    """Metaclass for EnumMap class definitions"""

    def __new__(cls, name, parents, dct):
        """
        Transform declared class attributes (expecing a 2-tuple of (K,V)).
        The attributes will become their "key", and __getitem__ access on
        the class will return the "value" of the mapping
        """
        mapping = {}

        # Transform the defined ENUM values. The first index of the value
        # is used as the "key", the second index is used as a value
        for name, val in dct.items():
            if type(val) == TupleType:
                mapping[val[0]] = val[1]
                dct[name] = val[0]
        dct['_map'] = mapping

        obj = super(EnumMapMeta, cls).__new__(cls, name, parents, dct)
        return obj

    def __init__(self, name, parents, dct):
        """
        Override self.__name__ to be the defined class name
        """
        self.__name__ = name

    def __iter__(self):
        return iter(self._map)

    def __getitem__(self, item):
        return self._map[item]

    def keys(self):
        return self._map.keys()

    def values(self):
        return self._map.values()

    def items(self):
        return self._map.items()

    def __repr__(self):
        return '<EnumMap:{}>'.format(self.__name__)

class EnumMap(object):
    """
    Easy, simple enum class. Define attributes as a 2-tuple of (key, value).
    The EnumMeta metaclass will transform the class to support iteration and [] getitem access
    for the
    values on the class, add a textual  in the _description dict.
    When iterating, _values will be the iteratee.

    class MyEnum(EnumMap):
        SOME_VALUE = (1, 'Some Value')
        SOME_OTHER_VALUE = (2, 'The other value')
    """

    __metaclass__ = EnumMapMeta
