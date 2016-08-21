import socket
import select


class AppServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('localhost', 8080))
        self.sock.setblocking(False)

        self.connections = []

        self.running = True

    def run(self):
        r, w, e = select.select([self.sock], [self.sock], [], 0)

        for i in r:
            if i == self.sock:
                message, addr = self.sock.recvfrom(1024)
                print('FROM CLIENT: ', message)

                msg_opcode = message[:4]
                if msg_opcode == b'CONN':
                    self.connections.append(addr)
                    print('CONNECTION CREATED FOR ADDR: ', addr)
                if msg_opcode == b'DRAW':
                    for conn in self.connections:
                        self.sock.sendto(message, conn)
