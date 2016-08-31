import pygame
import random
import socket
import select
from server import app_server
from src.client import Client
from src.net import Message

SERVER_ADDR = ('localhost', 8080)

class App(Client):
    def __init__(self):
        Client.__init__(self)

        self.window = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.window.fill((255, 255, 255))

        self.mouse_pos = None
        self.client_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.is_drawing = False

        self.connect_request = Message('CONN', ('string',))
        self.draw_message = Message('DRAW', ('int', 'int', 'int', 'int', 'int'))

        @self.message('DRAW')
        def draw_recv(message, addr):
            _, x, y, c0, c1, c2 = self.draw_message.unpack(message)
            pygame.draw.circle(self.window, (c0, c1, c2), (x, y), 5)

        self.set_server_addr(SERVER_ADDR)
        self.start()

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()

    def render(self, window):
        pygame.display.flip()

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                self.running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                m = self.draw_message.pack(self.mouse_pos[0], self.mouse_pos[1], self.client_color[0], self.client_color[1], self.client_color[2])
                self.simple_send(m)
                self.is_drawing = True
            if e.type == pygame.MOUSEBUTTONUP:
                self.is_drawing = False
            if e.type == pygame.MOUSEMOTION:
                if self.is_drawing:
                    m = self.draw_message.pack(self.mouse_pos[0], self.mouse_pos[1], self.client_color[0], self.client_color[1], self.client_color[2])
                    self.simple_send(m)
            if e.type == pygame.KEYDOWN and e.key == pygame.K_c:
                self.window.fill((255, 255, 255))
            if e.type == pygame.KEYDOWN and e.key == pygame.K_q:
                name = input('ENTER A NAME > ')
                m = self.connect_request.pack(name.encode())
                self.simple_send(m)
            if e.type == pygame.KEYDOWN and e.key == pygame.K_s:
                app_server.start()

    def run_app(self):
        self.update()
        self.render(self.window)
        self.handle_events(pygame.event.get())
        self.clock.tick()

    def close(self):
        self.shutdown()
        self.server.shutdown()
        pygame.quit()