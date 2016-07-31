import select
import socket
import struct
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
    VALID_DATAYPES = ['int', 'float', 'char', 'string', 'bool']

    def __init__(self, message_id, message_datatypes):
        self.message_id = message_id
        self.message_datatypes = message_datatypes

        self._msg_struct = struct.Struct(self._get_fmt_string())

    def _get_fmt_string(self):
        fmt = '>'
        for datatype in self.message_datatypes:
            if datatype in self.VALID_DATAYPES:
                if datatype == 'int':
                    fmt += 'I'
                if datatype == 'float':
                    fmt += 'f'
                if datatype == 'char':
                    pass
                if datatype == 'string':
                    pass
                if datatype == 'bool':
                    pass
            else:
                raise('Not valid datatype!')

        return fmt

    def pack(self, *args):
        for value in args:
            pass

    def unpack(self, binary_message):
        pass