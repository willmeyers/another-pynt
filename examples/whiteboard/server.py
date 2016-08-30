from src.server import Server
from src.net import Message

connect_request = Message('CONN', ('string',))
draw_message = Message('DRAW', ('string',))

app_server = Server('localhost', 8080)


@app_server.message('CONN')
def accept_connection(message, addr):
    _, name = connect_request.unpack(message)
    app_server.connect_client(name.decode(), addr)
    print('Got connect request -', name.decode())
    print(app_server.clients)


@app_server.message('DRAW')
def draw_recv(message, addr):
    app_server.simple_broadcast(message)