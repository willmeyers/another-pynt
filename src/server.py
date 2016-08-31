import socket
import threading
from collections import deque


class Server:
    default_config = {
        'HOST': 'localhost',
        'PORT': 8080,
        'MAX_RECV_BYTES': 1024,
    }

    def __init__(self, host, port, config=None):
        if config is not None:
            self.config = config
        else:
            self.config = self.default_config

        self.address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(False)
        self.sock.bind(self.address)

        self.incoming_messages = deque()
        self.outgoing_messages = deque()

        self.clients = {}

        self.message_map = {}

        self.running = True

    def update(self):
        pass

    def message(self, message_id):
        def decorator(f):
            self.message_map[message_id] = f
            return f

        return decorator

    def simple_send(self, message, addr):
        self.sock.sendto(message, addr)

    def simple_broadcast(self, message):
        for key, addr in self.clients.items():
            self.simple_send(message, addr)

    def connect_client(self, client_key, addr):
        print('connecting', client_key, addr)
        self.clients[client_key] = addr

    def disconnect_client(self, client_key):
        print('disconnecting', client_key)
        del self.clients[client_key]

    def run(self):
        while self.running:
            try:
                message, addr = self.sock.recvfrom(1024)

                if message:
                    self.message_map[message[:4].decode()](message, addr)

            except Exception:
                pass

    def start(self):
        print('Started server thread.')
        t = threading.Thread(target=self.run)
        t.start()

    def shutdown(self):
        for client_key, _ in self.clients.items():
            self.disconnect_client(client_key)

        self.sock.close()
        self.running = False