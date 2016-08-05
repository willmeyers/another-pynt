from src.server import Server

chat_server = Server('localhost', 8080)


@chat_server.message('CONN')
def connect(name):
    print('Got connect request')