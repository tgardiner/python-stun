from .attributes import (
    attribute,
    mapped_address,
    xor_mapped_address
)
from .request import request, request6
from .message import StunMessage
from .enumerations import (
    StunMessageType, StunMagicCookie, StunAttributeType,
    StunErrorCode, StunPort, StunsPort
)
__all__ = [
    'attribute',
    'mapped_address',
    'xor_mapped_address',
    'request',
    'request6',
    'StunMessage',
    'StunMessageType',
    'StunMagicCookie',
    'StunAttributeType',
    'StunErrorCode',
    'StunPort',
    'StunsPort'
]

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
