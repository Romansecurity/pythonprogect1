import paramiko

def ssh_comand(ip, port, user, passwd, cmd): #connected to server and execute cmd
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #allow to set up politics
    client.connect(ip, port=port, username=user, password=passwd)

    _st, stdout, stderr = client.exec_command(cmd)
    output = stdout.readlines() + stderr.readlines()
    if output:
        print("--Output--")
        for line in output:
            print(line.strip())

if __name__ == "__main__":
    import getpass
    user = input("Username: ")
    passwd = getpass.getpass()

    ip = input("Enter server IP: ") or "192.168.1.203"
    port = input("Enter port or <CR>: ") or 2222
    cmd = input("Enter command or <CR>: ") or "id"
    ssh_comand(ip, port, user, passwd, cmd)






