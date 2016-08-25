from src.server import Server
from src.net import Message

connect_request = Message(b'CONN', ('string',))
chat_message = Message(b'CHAT', ('string',))

chat_server = Server('localhost', 8080)


@chat_server.message(b'CONN')
def accept_connection(message, addr):
    _, name = connect_request.unpack(message)
    chat_server.connect_client(name.decode(), addr)
    print('Got connect request -', name.decode())


@chat_server.message(b'CHAT')
def chat_recv(message, addr):
    print(message)
    try:
        chat_server.simple_broadcast(message)
    except Exception as err:
        print(err)