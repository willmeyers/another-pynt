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
        """ Sends a packed and encoded message to the corresponding server address.

            message: A message instance
        """
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
    """ The Message object grants the ability to create simple packets of data.
        Messages must be given an identifier (4 bytes) and a tuple of datatypes
        that the message will store.

        example_message = Message('EXPL', ('int', 'int', 'float'))

    """
    VALID_DATAYPES = ['int', 'float', 'char', 'string', 'bool']

    def __init__(self, message_id, message_datatypes=None, max_str_len=32):
        self.message_id = message_id
        self.message_datatypes = message_datatypes

        self._msg_struct = struct.Struct(self._get_fmt_string())

    def _get_fmt_string(self):
        """ Returns the format string required for the message struct based on the datatpyes.

        """
        fmt = '>'
        for datatype in self.message_datatypes:
            if datatype in self.VALID_DATAYPES:
                if datatype == 'int':
                    fmt += 'I'
                if datatype == 'float':
                    fmt += 'f'
                if datatype == 'double':
                    fmt += 'd'
                if datatype == 'char':
                    fmt += 'c'
                if datatype == 'string':
                    fmt += 's'
                if datatype == 'bool':
                    fmt += 'b'
            else:
                raise('Error')

        return fmt

    def pack(self, *args):
        """ Returns a byte string given a list of arguments

            example_message = Message('EXPL', ('int', 'int', 'float'))
            message_to_send = example_message.pack(14, 89, 0.67)

        """
        return self._msg_struct.pack(*args)

    def unpack(self, raw_message):
        """ Returns a tuple with the unpacked values from the message.

        """
        return self._msg_struct.unpack(raw_message)


# Default and base messages for use
connect = Message('CONN')
keep_alive = Message('ALVE')