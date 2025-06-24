import socket

server_adress = ("192.168.1.203", 21)
message = "Hello"
bytestoSend = str.encode(message)
b = 4096

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto(bytestoSend, server_adress)

requests_message = client.recvfrom(b)

Message_server= "Message from server {}".format(requests_message)

print(Message_server)


