import socket
import selectors
from collections import deque


async read_wait(sock):
    await 'read_wait', sock

async write_wait(sock):
    await 'write_wait', sock


class EventLoop:
    """ This is a VERY SIMPLE implementation of an event loop. This is
    specifically designed for this particular application and UDP sockets.

    """
    def __init__(self):
        self.sel = selectors.DefaultSelector()

        self.ready = collections.deque()
        self.running = True

    def __repr__(self):
        pass

    def __str__(self):
        pass

    def __del__(self):
        pass

    def create_task(self, coro):
        pass

    def run(self):
        pass

