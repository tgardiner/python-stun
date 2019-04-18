import random
from .attributes.attribute import Attribute
from .enumerations import StunMessageType, StunMagicCookie, StunAttributeType


def _parse_attributes(buffer):
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


def _generate_transaction_id():
    return random.getrandbits(96).to_bytes(12, byteorder='big')


def _build_message_buffer(msg_type, transactionId, attributes):
    buffer = msg_type.value
    buffer += len(attributes).to_bytes(2, byteorder='big')
    buffer += StunMagicCookie.FULL.value
    buffer += transactionId
    buffer += attributes
    return buffer


class StunMessage:
    def __init__(self, buffer):
        self._buffer = buffer
        self._header_buffer = self._buffer[0:20]
        self._attribute_buffer = self._buffer[20:]
        self._attributes = _parse_attributes(self._attribute_buffer)

    @classmethod
    def create(cls, **kwargs):
        msg_type = kwargs.get('type', StunMessageType.REQUEST)
        transactionId = kwargs.get('transactionId', _generate_transaction_id())
        attributes = kwargs.get('attributes', b'')
        buffer = _build_message_buffer(msg_type, transactionId, attributes)
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
