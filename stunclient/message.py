import random
from .attributes import Attribute
from .enumerations import StunMessageType, StunMagicCookie, StunAttributeType


def parse_attributes(buffer):
    attributes = {}
    i = 0
    while i < len(buffer):
        attr_type = buffer[i:i+2]
        attr_len = int.from_bytes(buffer[i+2:i+4], byteorder='big')
        attr_value = buffer[i+4:i+4+attr_len]
        try:
            StunAttributeType(attr_type)
        except ValueError:
            # Unknown comprehension-optional attributes MUST be ignored
            # https://tools.ietf.org/html/rfc5389#section-7.3
            print('unknown type: ' + attr_type.hex())  # TODO: remove this
            pass
        else:
            attribute = Attribute.by_type(attr_type, attr_len, attr_value)
            if attribute.type not in attributes:
                attributes[attribute.type] = attribute.value
        i += 4 + attr_len
    return attributes


def generate_transaction_id():
    return random.getrandbits(96).to_bytes(12, byteorder='big')


def build_message(msg_type, transactionId, attributes):
    raw_bytes = msg_type.value
    raw_bytes += len(attributes).to_bytes(2, byteorder='big')
    raw_bytes += StunMagicCookie.FULL.value
    raw_bytes += transactionId
    raw_bytes += attributes
    return raw_bytes


class StunMessage:
    def __init__(self, buffer):
        self._buffer = buffer
        self._header_buffer = self._buffer[0:20]
        self._attribute_buffer = self._buffer[20:]
        self._attributes = parse_attributes(self._attribute_buffer)

    @classmethod
    def create(cls, **kwargs):
        msg_type = kwargs.get('type', StunMessageType.REQUEST)
        transactionId = kwargs.get('transactionId', generate_transaction_id())
        attributes = kwargs.get('attributes', b'')
        buffer = build_message(msg_type, transactionId, attributes)
        return cls(buffer)

    @property
    def type(self):
        return StunMessageType(self._buffer[0:2]).name

    @property
    def length(self):
        return int.from_bytes(self._buffer[2:4], byteorder='big')

    @property
    def transactionId(self):
        return int.from_bytes(self._buffer[8:20], byteorder='big')

    @property
    def attributes(self):
        return self._attributes

    @property
    def buffer(self):
        return self._buffer

    @property
    def header_buffer(self):
        return self._header_buffer

    @property
    def attribute_buffer(self):
        return self._attribute_buffer
