from .enumerations import (
    StunMagicCookie, StunAttributeType,
    StunMappedAddressFamily
)


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
        assert length == len(buffer)  # TODO: use logger
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
    def raw(self):
        return self._buffer

    @property
    def type(self):
        return self._type


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

    def __init__(self, type, length, buffer):
        assert type == self.static_type
        super().__init__(type, length, buffer)

    def _parse_buffer(self, buffer):
        self._family = StunMappedAddressFamily(buffer[1:2])
        self._port = int.from_bytes(buffer[2:4], byteorder='big')
        if self._family is StunMappedAddressFamily.IPV4:
            self._ip = ".".join([
                str(int.from_bytes(buffer[4:5], byteorder='big')),
                str(int.from_bytes(buffer[5:6], byteorder='big')),
                str(int.from_bytes(buffer[6:7], byteorder='big')),
                str(int.from_bytes(buffer[7:8], byteorder='big'))
            ])
        elif self._family is StunMappedAddressFamily.IPV6:
            raise Exception('not implemented')
        return {
            'family': self._family.name,
            'ip': self._ip,
            'port': self._port
        }


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

    def __init__(self, type, length, buffer):
        assert type == self.static_type
        super().__init__(type, length, buffer)

    def _xor_bytes(self, bytes1, bytes2):
        num1 = int.from_bytes(bytes1, byteorder='big')
        num2 = int.from_bytes(bytes2, byteorder='big')
        return num1 ^ num2

    def _decode_port(self, encoded_port):
        half_magic_cookie = StunMagicCookie.HALF.value
        return self._xor_bytes(encoded_port, half_magic_cookie)

    def _decode_ipv4_addr(self, raw_addr):
        magic_cookie = StunMagicCookie.FULL.value
        addr_int = self._xor_bytes(raw_addr, magic_cookie)
        addr_bytes = addr_int.to_bytes(4, 'big')
        oct1 = str(int.from_bytes(addr_bytes[0:1], byteorder='big'))
        oct2 = str(int.from_bytes(addr_bytes[1:2], byteorder='big'))
        oct3 = str(int.from_bytes(addr_bytes[2:3], byteorder='big'))
        oct4 = str(int.from_bytes(addr_bytes[3:4], byteorder='big'))
        return ".".join([oct1, oct2, oct3, oct4])

    def _parse_buffer(self, raw_value):
        self._family = StunMappedAddressFamily(raw_value[1:2])
        self._port = self._decode_port(raw_value[2:4])
        if self._family is StunMappedAddressFamily.IPV4:
            self._ip = self._decode_ipv4_addr(raw_value[4:8])
        elif self._family is StunMappedAddressFamily.IPV6:
            raise Exception('not implemented')
        return {
            'family': self._family.name,
            'ip': self._ip,
            'port': self._port
        }
