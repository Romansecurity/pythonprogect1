import socket

target_host = "localhost"
target_port = 5000

#SOCK_DGRAM- this is a type of socket that used transmit data in the form separate message 
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.send(b"GEt/HTTP1.1", (target_host, target_port))

#get data from any client ... accepts client data and a tuple of the clients's adress
data, addr = client.recvfrom(4096)

print(data.decode())
client.close()