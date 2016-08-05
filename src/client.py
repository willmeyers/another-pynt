import socket
import select
from .net import Connection


class Client:
    def __init__(self):
        self.connection = None
<<<<<<< HEAD
=======
        self.server_addr = None
>>>>>>> examples

        self.message_callbacks = {}

        self.running = True

    def connect(self, server_addr):
        self.server_addr = server_addr
        self.connection = Connection(self.server_addr)

<<<<<<< HEAD
=======
    def simple_send(self, message):
        self.connection.simple_send(message)

>>>>>>> examples
    def message(self, message_id):
        def decorator(f):
            self.message_callbacks[message_id] = f
            return f

        return decorator

    def run(self):
        pass