import socket
import select
import threading
from collections import deque


class Client:
    default_config = {
        'SERVER_ADDR': None,
        'MAX_RECV_BYTES': 1024,
    }

    def __init__(self, config=None):
        if config is not None:
            self.config = config
        else:
            self.config = self.default_config

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #self.sock.setblocking(False)
        self.sock.bind(('', 0))

        self.incoming_messages = deque()
        self.outgoing_messages = deque()
        self.ack_messages = deque()

        self.message_map = {}

        self.running = True

    def set_server_addr(self, addr):
        self.config['SERVER_ADDR'] = addr

    def simple_send(self, message):
        """ Sends an unreliable message to the configured server address. Simple
        send is recommended for bulk sends. Depending on the application; sending
        keyboard input, updating variables... Using a  deque for future use.

        :param message: a message object
        """
        self.outgoing_messages.append(message)
        while self.outgoing_messages:
            m = self.outgoing_messages.pop()
            self.sock.sendto(m, self.config['SERVER_ADDR'])

    def message(self, message_id):
        """ A decorator function for easy message rule mapping.

            @message('CHAT')
            def chat_message(text):
                # display chat message
                ...

        :param message_id: the message id
        """
        def decorator(f):
            self.message_map[message_id] = f
            return f

        return decorator

    def run(self):
        while self.running:
            try:
                message, addr = self.sock.recvfrom(1024)

                if message:
                    self.message_map[message[:4].decode()](message, addr)

            except Exception:
                pass

    def start(self):
        print('Started client thread.')
        t = threading.Thread(target=self.run)
        t.start()

    def shutdown(self):
        self.sock.close()
        self.running = False