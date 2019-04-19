from python_stun.attributes.attribute import Attribute
from python_stun.enumerations import (
    StunMagicCookie, StunAttributeType,
    StunMappedAddressFamily
)
from ipaddress import ip_address


class _XORDecoder:
    def __init__(self, XORvalue):
        self._XORvalue = int.from_bytes(XORvalue, byteorder='big')

    def _xor_buffer(self, buffer):
        int_buffer = int.from_bytes(buffer, byteorder='big')
        return self._XORvalue ^ int_buffer

    def decode(self, buffer):
        xord_buffer = self._xor_buffer(buffer)
        len_xord_buffer = (xord_buffer.bit_length() + 7) // 8
        return xord_buffer.to_bytes(len_xord_buffer, byteorder='big')

    def decode_int(self, buffer):
        return self._xor_buffer(buffer)


class XORMappedAddress(Attribute):
    #  0                   1                   2                   3
    #  0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # |x x x x x x x x|    Family     |         X-Port                |
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    # |                X-Address (Variable)
    # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    #               Format of XOR-MAPPED-ADDRESS Attribute
    #          https://tools.ietf.org/html/rfc5389#section-15.2
    static_type = StunAttributeType['XORMAPPEDADDRESS'].value

    def __init__(self, type, length, buffer, transaction_id):
        assert type == self.static_type
        self._xor_value_map = {
            StunMappedAddressFamily.IPV4: StunMagicCookie.FULL.value,
            StunMappedAddressFamily.IPV6: StunMagicCookie.FULL.value +
            transaction_id.to_bytes((transaction_id.bit_length() + 7) // 8, byteorder='big')
        }
        super().__init__(type, length, buffer, transaction_id)

    def _decode_port(self, encoded_port):
        decoder = _XORDecoder(StunMagicCookie.HALF.value)
        return decoder.decode_int(encoded_port)

    def _decode_ip_addr(self, encoded_ip_addr, family):
        decoder = _XORDecoder(self._xor_value_map[family])
        return ip_address(decoder.decode(encoded_ip_addr))

    def _parse_buffer(self, buffer):
        self._family = StunMappedAddressFamily(buffer[1:2])
        self._port = self._decode_port(buffer[2:4])
        self._ip = self._decode_ip_addr(buffer[4:self._length], self._family)
        return {
            'family': self._family.name,
            'ip': self._ip,
            'port': self._port
        }
