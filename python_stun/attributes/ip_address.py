from python_stun.enumerations import StunMappedAddressFamily


class _Decoder:
    def decode(buffer):
        return buffer


class _IPAddress:
    def __init__(self, family, buffer, decoder):
        self._family = StunMappedAddressFamily(family).name
        self._decoder = decoder
        self._buffer = decoder.decode(buffer)
        self._value = self._parse_buffer(self._buffer)

    def _parse_buffer(self, buffer):
        return {}

    @classmethod
    def by_family(cls, family, buffer, decoder=_Decoder):
        classmap = {c.static_family: c for c in cls.__subclasses__()}
        return classmap[family](family, buffer, decoder)

    @property
    def family(self):
        return self._family

    @property
    def buffer(self):
        return self._buffer

    @property
    def value(self):
        return self._value


class _IPv4Address(_IPAddress):
    static_family = StunMappedAddressFamily['IPV4'].value

    def __init__(self, family, buffer, decoder):
        assert family == self.static_family
        super().__init__(family, buffer, decoder)

    def _parse_buffer(self, buffer):
        oct1 = str(int.from_bytes(buffer[0:1], byteorder='big'))
        oct2 = str(int.from_bytes(buffer[1:2], byteorder='big'))
        oct3 = str(int.from_bytes(buffer[2:3], byteorder='big'))
        oct4 = str(int.from_bytes(buffer[3:4], byteorder='big'))
        return ".".join([oct1, oct2, oct3, oct4])


class _IPv6Address(_IPAddress):
    static_family = StunMappedAddressFamily['IPV6'].value

    def __init__(self, family, buffer, decoder):
        assert family == self.static_family
        raise Exception('not implemented')  # TODO: Implement
        super().__init__(family, buffer, decoder)
