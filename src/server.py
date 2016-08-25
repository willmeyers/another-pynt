import socket
import threading
from collections import deque


class Server:
    default_config = {
        'HOST': 'localhost',
        'PORT': 8080,
        'MAX_RECV_BYTES': 1024,
        'TICK_RATE': 30,
        'ACK_UPDATE_RATE': 1000 # in ms
    }

    def __init__(self, host, port, config=None):
        if config is not None:
            self.config = config
        else:
            self.config = self.default_config
        # Have to setup host and port config

        self.address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(False)
        self.sock.bind(self.address)

        self.incoming_messages = deque()
        self.outgoing_messages = deque()
        self.messages_needing_ack = deque()

        self.clients = []
        self.pending_disconnects = []

        self.message_map = {}

        self.running = True

    def update(self):
        pass

    def add_message_rule(self, message_id):
        pass

    def message(self, message_id):
        def decorator(f):
            self.add_message_rule(message_id)
            return f

        return decorator

    def read_message(self, message, addr):
        message_id = message[:4].decode()
        print(message_id)
        self.message_callbacks[message_id](message)

    def simple_send(self, message, addr):
        pass

    def reliable_send(self, message, addr):
        pass

    def simple_broadcast(self, message):
        for client in self.clients:
            self.simple_send(message, client)

    def reliable_broadcast(self, message):
        pass

    def refresh_acks(self):
        while self.messages_needing_ack:
            msg = self.messages_needing_ack.pop()
            self.simple_send(msg, msg.addr)

    def run(self):
        while self.running:
            try:
                message, addr = self.sock.recvfrom(1024)

                if message:
                    print(message[:4], message)

            except Exception:
                pass

    def start(self):
        print('Started server thread.')
        t = threading.Thread(target=self.run)
        t.start()

    def shutdown(self):
        self.sock.close()
        self.running = False


class ServerTest:
    def __init__(self, hostname, port, max_recv_bytes=1024, **kwargs):
        self.hostname = hostname
        self.port = port
        self.max_recv_bytes = max_recv_bytes
        self.kwargs = kwargs

        self.message_map = {}

    def __del__(self):
        pass

    #   Public methods
    def message(self, message_id):
        def decorator(f):
            self.message_map[message_id] = f

            return f

        return decorator

    def connect_client(self):
        pass

    def disconnect_client(self):
        pass

    def start(self):
        pass

    def close(self):
        pass

    #   Private methods
    def _init_socket(self):
        pass

    def _run(self):
        pass