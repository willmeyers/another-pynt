import pygame
import random
import socket
import select
from server import AppServer
from src.net import Message


class App:
    def __init__(self):
        self.window = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()

        self.mouse_pos = None
        self.client_color = (random.randint(50, 255),random.randint(50, 255),random.randint(50, 255))
        self.is_drawing = False

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', 0))
        self.sock.setblocking(False)

        self.running = True

        self.server = AppServer()

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()

    def render(self, window):
        pygame.display.flip()

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                self.running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.circle(self.window, self.client_color, self.mouse_pos, 5)
                m = b'DRAW'+str(self.mouse_pos[0]).encode()+str(self.mouse_pos[1]).encode()
                self.sock.sendto(m, ('localhost', 8080))
                self.is_drawing = True
            if e.type == pygame.MOUSEBUTTONUP:
                self.is_drawing = False
            if e.type == pygame.MOUSEMOTION:
                if self.is_drawing:
                    pygame.draw.circle(self.window, self.client_color, self.mouse_pos, 5)
                    m = b'DRAW'+str(self.mouse_pos[0]).encode()+str(self.mouse_pos[1]).encode()
                    self.sock.sendto(m, ('localhost', 8080))
            if e.type == pygame.KEYDOWN and e.key == pygame.K_c:
                self.window.fill((0, 0, 0))
            if e.type == pygame.KEYDOWN and e.key == pygame.K_s:
                pass

    def run(self):
        self.update()
        self.render(self.window)
        self.handle_events(pygame.event.get())
        self.server.run()
        self.clock.tick(60)

        r, w, e = select.select([self.sock], [self.sock], [])
        for i in r:
            if i == self.sock:
                message, addr = self.sock.recvfrom(1024)
                print('FROM SERVER: ', message)
                if message[:4] == b'DRAW':
                    pygame.draw.circle(self.window, (255, 255, 255), (self.mouse_pos[0]-50, self.mouse_pos[1]), 5)


    def close(self):
        pygame.quit()