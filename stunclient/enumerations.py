from enum import Enum


class StunMessageType(Enum):
    # "0x%#04d" % int(hex(0x0001 & 0x0110)[2:])
    REQUEST = b'\x00\x01'  # 0x0001
    INDICATION = b'\x00\x10'  # 0x0010
    SUCCESS_RESP = b'\x01\x01'  # 0x0101
    ERROR_RESP = b'\x01\x11'  # 0x0111


class StunMagicCookie(Enum):
    HALF = b'!\x12'  # 0x2112
    FULL = b'!\x12\xa4B'  # 0x2112a442


class StunRetransmisionValues(Enum):
    # https://tools.ietf.org/html/rfc5389#section-7.2.1
    RTO: 0.5  # 500ms
    RM: 16
    RETRANSMISSIONS: 7


class StunAttributeType(Enum):
    # Reserved = b'\x00\x00' # 0x0000
    MAPPEDADDRESS = b'\x00\x01'  # 0x0001
    # Reserved = b'\x00\x02' # 0x0002 was RESPONSE-ADDRESS
    # Reserved = b'\x00\x03' # 0x0003 was CHANGE-ADDRESS
    # Reserved = b'\x00\x04' # 0x0004 was SOURCE-ADDRESS
    # Reserved = b'\x00\x05' # 0x0005 was CHANGED-ADDRESS
    USERNAME = b'\x00\x06'  # 0x0006
    # Reserved = b'\x00\x07' # 0x0007 was PASSWORD
    MESSAGEINTEGRITY = b'\x00\x08'  # 0x0008
    ERRORCODE = b'\x00\t'  # 0x0009
    UNKNOWNATTRIBUTES = b'\x00\n'  # 0x000a
    # Reserved = b'\x00\x0b' # 0x000b was REFLECTED-FROM
    REALM = b'\x00\x14'  # 0x0014
    NONCE = b'\x00\x15'  # 0x0015
    XORMAPPEDADDRESS = b'\x00 '  # 0x0020
    SOFTWARE = b'\x80"'  # 0x8022
    ALTERNATESERVER = b'\x80#'  # 0x8023
    FINGERPRINT = b'\x80('  # 0x8028


class StunMappedAddressFamily(Enum):
    IPV4 = b'\x01'  # 0x01
    IPV6 = b'\x02'  # 0x02


class StunErrorCode(Enum):
    TRYALTERNATE = 300
    BADREQUEST = 400
    UNAUTHORIZED = 401
    UNKNOWNATTRIBUTE = 420
    STALENONCE = 438
    SERVERERROR = 500


class StunPort(Enum):
    UDP = 3478
    TCP = 3478


class StunsPort(Enum):
    UDP = 5349
    TCP = 5349
