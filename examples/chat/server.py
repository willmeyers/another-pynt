from src.server import Server
from src.net import Message

connect_request = Message(b'CONN', ('string',))

chat_server = Server('localhost', 8080)

@chat_server.message(b'CONN')
def accept_connection(message):
    _, name = connect_request.unpack(message)
    print('Got connect request -', name.decode())