import socket
import select
from collections import deque


class Client:
    server_address = None

    default_config = {
        'MAX_RECV_BYTES': 1024,
        'TICK_RATE': 30,
    }

    def __init__(self, config=None):
        if config is not None:
            self.config = config
        else:
            self.config = self.default_config

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(False)
        self.sock.bind(('', 0))

        self.incoming_messages = deque()
        self.outgoing_messages = deque()
        self.ack_messages = deque()

        self.server_addr = None

        self.message_map = {}

        self.running = True

    def simple_send(self, message):
        pass

    def add_message_rule(self, message_id):
        pass

    def message(self, message_id):
        def decorator(f):
            self.add_message_rule(message_id)
            return f

        return decorator

    def run(self):
        r, w, e = select.select([self.sock], [self.sock], [], 0)
        for i in r:
            if i == self.sock:
                message, addr = self.sock.recvfrom(1024)
                print(message)
                self.incoming_messages.appendleft((message, addr))

        for j in w:
            if j == self.sock:
                if self.outgoing_messages:
                    pass
                    #self.sock.sendto(self.outgoing_messages.pop(), recv_addr)