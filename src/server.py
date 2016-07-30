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

        self.config = {}

        self.received_messages = deque()
        self.outgoing_messages = deque()
        self.messages_needing_ack = deque()

        self.clients = {}
        self.pending_disconnects = []

        self.message_callbacks = {}

        self.running = True

    def load_config_from_file(self):
        pass

    def message(self, message_id):
        def decorator(f):
            self.message_callbacks[message_id] = f
            return f

        return decorator

    def read_buffer(self, buffer, addr):
        pass

    def listen(self):
        while self.running:
            try:
                message_buffer, addr = self.sock.recvfrom(self.config['RECV_BYTES'])

                if message_buffer:
                    self.received_messages.appendleft(message_buffer)
            except Exception:
                pass

    def start(self):
        t = threading.Thread(target=self.listen)
        t.start()

    def shutdown(self):
        self.sock.close()
        self.running = False