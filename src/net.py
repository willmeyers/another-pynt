from collections import deque


class Connection:
    def __init__(self):
        self.seq_number = 0

        self.received_messages = deque()
        self.outgoing_messages = deque()
        self.messages_needing_ack = deque()


class Message:
    def __init__(self):
        pass