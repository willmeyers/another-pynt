from src.server import Server

chat_server = Server('localhost', 8080)


@chat_server.message(b'CONN')
def accept_connection():
    print('Got connect request')