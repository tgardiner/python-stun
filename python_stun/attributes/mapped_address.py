from python_stun.attributes.attribute import Attribute
from python_stun.enumerations import (
    StunAttributeType,
    StunMappedAddressFamily
)
from ipaddress import ip_address


class MappedAddress(Attribute):
    #  0                   1                   2                   3
    #  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # |0 0 0 0 0 0 0 0|    Family     |           Port                |
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # |                                                               |
    # |                 Address (32 bits or 128 bits)                 |
    # |                                                               |
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #                 Format of MAPPED-ADDRESS Attribute
    #          https://tools.ietf.org/html/rfc5389#section-15.1
    static_type = StunAttributeType['MAPPEDADDRESS'].value

    def __init__(self, type, length, buffer, transaction_id):
        assert type == self.static_type
        super().__init__(type, length, buffer, transaction_id)

    def _parse_buffer(self, buffer):
        self._family = StunMappedAddressFamily(buffer[1:2])
        self._port = int.from_bytes(buffer[2:4], byteorder='big')
        self._ip = str(ip_address(buffer[4:self._length]))
        return {
            'family': self._family.name,
            'ip': self._ip,
            'port': self._port
        }
