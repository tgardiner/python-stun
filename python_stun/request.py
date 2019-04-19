import socket
from .enumerations import StunPort
from .message import StunMessage


def request(host, **kwargs):
    port = kwargs.get('port', StunPort.UDP.value)
    message = kwargs.get('message', StunMessage.create())
    timeout = kwargs.get('initial_timeout', 0.5)
    attempts = kwargs.get('attempts', 7)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        _set_sock_opts(s, timeout)
        return _send(s, host, port, message, attempts)


def request6(host, **kwargs):
    port = kwargs.get('port', StunPort.UDP.value)
    message = kwargs.get('message', StunMessage.create())
    timeout = kwargs.get('initial_timeout', 0.5)
    attempts = kwargs.get('attempts', 7)
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as s:
        _set_sock_opts(s, timeout)
        return _send(s, host, port, message, attempts)


def _set_sock_opts(s, timeout):
    s.settimeout(timeout)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # s.bind(('0.0.0.0', 54320)) # DO WE NEED THIS?


def _send(s, host, port, message, attempts):
    for attempt in range(1, attempts + 1):
        s.sendto(message.buffer, (host, port))
        try:
            resp_buffer, _ = s.recvfrom(2048)
        except socket.error:
            print(f"Attempt: {attempt} timeout")  # TODO: use logger
            # Exponential backoff
            s.settimeout(s.timeout * 2)
            if attempt == attempts:
                raise
        else:
            return StunMessage(buffer=resp_buffer)
