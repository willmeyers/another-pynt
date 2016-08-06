import socket
import select
from .net import Connection


class Client:
    connection = Connection
    server_address = None

    default_config = {
        'MAX_RECV_BYTES': 1024
    }

    def __init__(self):
        self.server_addr = None

        self.message_map = {}

        self.running = True

    def connect(self, server_addr):
        self.server_addr = server_addr
        self.connection = Connection(self.server_addr)

    def simple_send(self, message):
        self.connection.simple_send(message)

    def add_message_rule(self, message_id):
        pass

    def message(self, message_id):
        def decorator(f):
            self.message_callbacks[message_id] = f
            return f

        return decorator

    def run(self):
        pass