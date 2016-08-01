import socket
import select
from .net import Connection


class Client:
    def __init__(self):
        self.connection = None

        self.message_callbacks = {}

        self.running = True

    def connect(self, server_addr):
        self.connection = Connection(server_addr)

    def simple_send(self, message):
        pass

    def message(self, message_id):
        def decorator(f):
            self.message_callbacks[message_id] = f
            return f

        return decorator

    def run(self):
        pass