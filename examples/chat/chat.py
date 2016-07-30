import pygame
from src.client import Client
from server import chat_server


class Chat:
    def __init__(self):
        self.window = pygame.display.set_mode((640, 480))
        self.running = True

    def update(self):
        pass

    def render(self, window):
        pygame.display.flip()

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.QUIT:
                self.running = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_s:
                    chat_server.start()

    def run(self):
        while self.running:
            self.update()
            self.render(self.window)
            self.handle_events(pygame.event.get())

        chat_server.shutdown()

c = Chat()
c.run()