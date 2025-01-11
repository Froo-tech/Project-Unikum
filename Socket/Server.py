import socket

HOST = (socket.gethostname(), 10000)

s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(HOST)
s.listen()
print('Слушаю подключения: ')

while True:
    conn, addr = s.accept()
    print(f"Подключен {addr}")
    res = b"hello"
    conn.send(res)