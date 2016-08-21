import socket
import select


class AppServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('localhost', 8080))
        self.sock.setblocking(False)

        self.running = True

    def run(self):
        r, w, e = select.select([self.sock], [self.sock], [], 0)

        for i in r:
            if i == self.sock:
                message, addr = self.sock.recvfrom(1024)
                print('FROM CLIENT: ', message)
                self.sock.sendto(message, addr)
