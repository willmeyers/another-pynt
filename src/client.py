import socket
from collections import deque


class Client:
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.setblocking(False)

        self.config = None
        self.running = True

        self.sent_messages = deque()
        self.recv_messages = deque()
        self.ask_messages = deque()

        self.messages = {}

    def __repr__(self):
        pass
    
    def __str__(self):
        pass

    def __del__(self):
        pass

    def message(self, command):
        pass

    def simple_send(self, message):
        pass

    def reliable_send(self, message):
        pass

    async def _send(self, message):
        pass

    async def _recv(self):
        pass
