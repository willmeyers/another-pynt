#!usr/bin/env python

import socket
import threading
import time


class Peer:
    def __init__(self):
        self.peers = {}
        self.sock = None
        
    def start_listener(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('127.0.0.1', port))
        self.sock.listen(5)

        print('[MESSAGE] Started listening on port', port)

    def listen_for_peers(self):
        while True:
            conn, addr = self.sock.accept()
            print('[MESSAGE] A client connected to you from', addr)

            self.peers[addr] = conn
            t = threading.Thread(target=self.handle_peer, args=[conn, addr])
            t.start()
            print('[MESSAGE] Started a new tread to handle new connetion at', t)

    def handle_peer(self, conn, addr):
        while True:
            try:
                data = conn.recv(1024)
                print('[%s SAYS] %s' % (addr, data))
            except Exception as err:
                pass
        self.peers[addr] = None
        conn.close()
        print('[MESSAGE] Disconnected peer', addr)


p = Peer()
p.start_listener(8080)
p.listen_for_peers()
