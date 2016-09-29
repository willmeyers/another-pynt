from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
import socket


sel = DefaultSelector()

def accept(sock, mask):
    conn, addr = sock.accept()
    print('Got: ', addr)
    conn.setblocking(False)
    sel.register(conn, EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1024)
    if data:
        print('HEY: ', data)
        conn.send(data)

    else:
        print('Closing')
        sel.unregister(conn)
        conn.close()

sock = socket.socket()
sock.bind(('localhost', 8080))
sock.listen(1)
sock.setblocking(False)
sel.register(sock, EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)



