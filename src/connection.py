import socket
import select
from collections import deque


class Connection:
    def __init__(self, server_addr):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(False)
        self.sock.bind(('', 0))

        self.server_addr = server_addr
        self.seq_number = 0

        self.received_messages = deque()
        self.outgoing_messages = deque()

        self.recv_messages = deque()
        self.sent_messages = deque()
        self.ack_messages = deque()

    def simple_send(self, message):
        """ Sends a packed and encoded message to the corresponding server address.

            message: A message instance
        """
        self.sock.sendto(message, self.server_addr)

    def reliable_send(self, message):
        # TODO
        # Sends a reliable message
        pass

    def update(self):
        pass

    def _send_and_recv(self, sender_sock, recv_addr):
        r, w, e = select.select([sender_sock], [sender_sock], [], 0)
        for i in r:
            if i == sender_sock:
                message, addr = sender_sock.recvfrom(1024)
                print(message)
                self.received_messages.appendleft((message, addr))

        for j in w:
            if j == sender_sock:
                if self.outgoing_messages:
                    sender_sock.sendto(self.outgoing_messages.pop(), recv_addr)