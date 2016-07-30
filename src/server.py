import socket
import threading
from collections import deque


class Server:
    def __init__(self, host, port):
        self.address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(False)
        self.sock.bind(self.address)

        self.received_messages = deque()
        self.outgoing_messages = deque()
        self.pending_ack_messages = deque()

    def load_config_from_file(self):
        pass

    def read_buffer(self):
        pass

    def start(self):
        pass

    def shutdown(self):
        pass