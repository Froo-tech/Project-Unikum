import socket

HOST = (socket.gethostname(), 10000)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(HOST)
print("Подключение к ", HOST)
msg = client.recv(2048)
print(msg.decode("UTF-8"))
