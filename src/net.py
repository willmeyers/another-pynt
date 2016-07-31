import select
import socket
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

    def simple_send(self, message):
        self.sock.sendto(message, self.server_addr)

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


class Message:
    def __init__(self, message_id, *message_data):
        self.message_id = message_id
        self.message_data = message_data

    def pack(self, *args):
        for value in args:
            pass

    def unpack(self):
        pass