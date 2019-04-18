from python_stun.enumerations import StunAttributeType


class Attribute:
    #  0                   1                   2                   3
    #  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # |         Type                  |            Length             |
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # |                         Value (variable)                ....
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #                     Format of STUN Attributes
    #             https://tools.ietf.org/html/rfc5389#page-31
    def __init__(self, type, length, buffer):
        assert length == len(buffer)
        self._type = StunAttributeType(type).name
        self._length = length
        self._buffer = buffer
        self._value = self._parse_buffer(self._buffer)

    def _parse_buffer(self, buffer):
        return {}

    @classmethod
    def by_type(cls, type, length, buffer):
        classmap = {c.static_type: c for c in cls.__subclasses__()}
        return classmap[type](type, length, buffer)

    @property
    def value(self):
        return self._value

    @property
    def length(self):
        return self._length

    @property
    def buffer(self):
        return self._buffer

    @property
    def type(self):
        return self._type
