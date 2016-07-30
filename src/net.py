import select
from collections import deque


class Connection:
    def __init__(self):
        self.seq_number = 0

        self.received_messages = deque()
        self.outgoing_messages = deque()
        self.messages_needing_ack = deque()

    def simple_send(self, message):
        pass

    def reliable_send(self, message):
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
                message = Message()
                self.outgoing_messages.appendleft(message.pack())

class Message:
    def __init__(self):
        pass

    def pack(self):
        pass

    def unpack(self):
        pass