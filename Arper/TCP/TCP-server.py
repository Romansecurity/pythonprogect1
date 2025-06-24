import socket
import threading   #Multithreading library

ip = "0.0.0.0"
port = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5) #No more than five connections
    print(f"[*]Listening on {ip}:{port}")

    while True:
        client, address = server.accept()
        print(f'[*]Accepted connection from {address[0]}:{address[1]}') 
        #accepts a function that  will need to be executed in the stream ...accepts tuple argument
        client_handler = threading.Thread(target=handle_client, args=(client,)) #creating a new stream

        client_handler.start()

def handle_client(client_socket):
    #wrapping the context manager 
    with client_socket as sock:
        requests = sock.recv(1024)
        print(f'[*]Received :{requests.decode("utf-8")}')
        sock.send(b'ACD')
    
if __name__ == "__main__":
    main()
    


