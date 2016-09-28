import socket
import asyncio
from collections import deque


class UDPTest:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        print(message)


class Server:
    default_config = {
        'SERVER_ADDRESS': None, 
        'MAX_CONNECTIONS': 16,
        'MAX_RECV_BYTES': 1024,
    }

    def __init__(self):
        print('Server thread started!')
        
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.setblocking(False)
        
        self.running = True
        self.server_addr = None
        self.config = self.default_config

        self.sent_messages = deque()
        self.recv_messages = deque()
        self.ack_messages = deque()

        self.messages = {}
   
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.l = self.loop.create_datagram_endpoint(UDPTest, local_addr=(self.server_addr))

    def __repr__(self):
        return 'Add useful info here!'

    def __str__(self):
        return 'Add useful info'

    def __del__(self):
        self.running = False 
        self._socket.close()
        print('Server stopped')

    def bindto(self, addr):
        self.server_addr = addr
        self.config['SERVER_ADDR'] = self.server_addr
        self._socket.bind(addr)

    def message(self, command):
        pass

    def simple_send(self, message):
        pass

    def reliable_send(self, message):
        pass

    def start(self):
        if self.running:
            print('STARTED!')
            t, p = self.loop.run_until_complete(self.l)
            self.loop.run_forever()

from threading import Thread
def hello():
    s = Server()
    s.bindto(('localhost', 8080))
    s.start()
t = Thread(target=hello, args=())
t.start()
