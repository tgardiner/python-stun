from .request import request
from .message import StunMessage
from .enumerations import (
    StunMessageType, StunMagicCookie, StunAttributeType,
    StunErrorCode, StunPort, StunsPort
)
__all__ = [
    'request',
    'StunMessage',
    'StunMessageType',
    'StunMagicCookie',
    'StunAttribute',
    'StunErrorCode',
    'StunPort',
    'StunsPort'
]

# Set default logging handler to avoid "No handler found" warnings.
import logging
from logging import NullHandler

logging.getLogger(__name__).addHandler(NullHandler())
