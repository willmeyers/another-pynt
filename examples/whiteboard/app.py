import pygame
import random
import socket
from server import server
from src.net import Message


class App:
    def __init__(self):
        self.window = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()

        self.mouse_pos = None
        self.client_color = (random.randint(50, 255),random.randint(50, 255),random.randint(50, 255))
        self.is_drawing = False

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)

        self.draw_message = Message(b'DRAW', ('int', 'int'))

        self.running = True

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
                self.is_drawing = True
            if e.type == pygame.MOUSEBUTTONUP:
                self.is_drawing = False
            if e.type == pygame.MOUSEMOTION:
                if self.is_drawing:
                    pygame.draw.circle(self.window, self.client_color, self.mouse_pos, 5)
                    m = self.draw_message.pack(self.mouse_pos[0], self.mouse_pos[1])
                    self.sock.sendto(m, ('localhost', 8080))
            if e.type == pygame.KEYDOWN and e.key == pygame.K_c:
                self.window.fill((0, 0, 0))
            if e.type == pygame.KEYDOWN and e.key == pygame.K_s:
                server.start()

    def run(self):
        self.update()
        self.render(self.window)
        self.handle_events(pygame.event.get())
        self.clock.tick(60)

    def close(self):
        pygame.quit()
        server.shutdown()