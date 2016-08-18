from src.server import Server

server = Server('localhost', 8080)

@server.message(b'DRAW')
def draw(x, y):
    print(x, y)