import socket

target_host = "192.168.64.2"
target_port = 25

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))

client.send(b'GET/ HTTP1.1')

response = client.recv(4096)

print(response.decode())
client.close()


