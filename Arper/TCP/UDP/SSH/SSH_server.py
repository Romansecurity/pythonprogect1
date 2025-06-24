import os
import paramiko
import threading
import socket
import sys

CWD = os.path.dirname(os.path.realpath(__file__)) #return the name of the directory in the specified path/compressed file path
HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))#RSA key- is used for secure data transfer/join - connected paths

class Server(paramiko.ServerInterface): #support SSH
    def __init__(self):
        self.event = threading.Event()# mechanism of communication
    
    def check_channel_request(self, kind, chanid): #kind-the type of channel, that the client would like to open/chanid-some number, that identifies the channel
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, username, password):
        if (username == "roman") and (password == "secret"):
            return paramiko.AUTH_SUCCESSFUL

if __name__ == "__main__":
    server = "192.168.64.2" #cmd- ifconfig
    ssh_port = 2222
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print("[+]Listening connection...")
        client, addr = sock.accept()
    except Exception as e:
        print("[-]Listen failed..." + str(e))
        sys.exit(1)
    else:
        print(f"[+]Got a connection to {addr}")
    
    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(HOSTKEY)
    server=Server()
    bhSession.start_server(server=server)

    chan = bhSession.accept(20) #??????
    if chan is None:
        print("***No chanel")
        sys.exit(1)
    
    print("[+]Authenticated!")
    print(chan.recv(1024).decode()) #"client connected"
    chan.send("Welcome to bh_ssh")
    try:
        while True:
            command = input("Enter a command:") #input with SSH_server
            if command != "exit":
                chan.send(command) #transport ssh_client
                r = chan.recv(8192) #accept to ssh_server
                print(r.decode())
            else:
                chan.send("exit")
                print("exiting")
                bhSession.close()
                break
    except KeyboardInterrupt:
        bhSession.close()






        


