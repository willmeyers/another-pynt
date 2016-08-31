from src.server import Server
from src.net import Message

connect_request = Message('CONN', ('string',))
chat_message = Message('CHAT', ('string', 'string'))

chat_server = Server('localhost', 8080)


@chat_server.message('CONN')
def accept_connection(message, addr):
    _, name = connect_request.unpack(message)
    chat_server.connect_client(name.decode(), addr)
    m = chat_message.pack(name.decode(), b'Connected to server!')
    chat_server.simple_broadcast(chat_message)
    print('Got connect request -', name.decode())


@chat_server.message('CHAT')
def chat_recv(message, addr):
    chat_server.simple_broadcast(message)