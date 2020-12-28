import logging

from railcmd.exceptions import ProtocolError


def expect(a, b):
    if a != b:
        raise ProtocolError(f'{b} expected, {a} received')


log = logging.getLogger()