import getpass
import os
import socket
import select #stdin, stdout, stddr
import sys
import threading
from optparse import OptionParser
import paramiko

SSH_port = 22
default_port = 4000

g_verbose = True

def handler(chan, host, port):
    sock = socket.socket()
    try:
        sock.connect((host, port))
    except Exception as e:
        verbose("Forwarding requests to %s:%d failed: %r" % (host, port, e))
        return
    
    verbose(
        "Connected! Tunnel open %r -> %r -> %r"
        % (chan.origin_addr, chan.getpeername(), (host, port))#?
    )
    while True:
        r, w, x = select.select([sock, chan], [], [])
        if sock in r:
            data = sock.recv(1024)
            if len(data) == 0:
                break
            chan.send(data)
        if chan in r:
            data = chan.recv(1024)
            if len(data) == 0:
                break
            sock.send(data)
    chan.close()
    sock.close()
    verbose("Tunnel closed from %r" % (chan.origin_addr,))


def reverse_forward_tunnel(server_port, remote_host, remote_port, transport):
    transport.request_port_forward("", server_port)
    while True:
        chan = transport.accept(1000)
        if chan is None:
            continue
        thr = threading.Thread(
            target=handler, args=(chan, remote_host, remote_port)
        )
        thr.setDaemon(True)
        thr.start()

def verbose(s):
    if g_verbose:
        print(s)

HELP = """\
Set up a reverse forwarding tunnel across on the SSH-server, using paramiko.A
port on the SSH server (given with -p) is forwarded across an SSH-session back
to the local machine, and out to a remote site from this network.This is simular 
to the open -R option.
"""

def get_host_port(spec, default_port):
    #parse hostname:22 into a host and port, with the port optional 
    args = (spec.split(":", 1) + [default_port])[:2]
    args[1] = int(args[1])
    return args[0], args[1]

def parse_options():
    global g_verbose

    parser = OptionParser(
        usage="usage: %prog [options] <ssh_server>[:<server-port>]",
        version="%prog 1.0",
        description=HELP,
    )
    parser.add_option(
        "-q", 
        "--quit", 
        action='store_false', 
        dest="verbose", 
        default=True, 
        help="squelch all information output",
    )
    parser.add_option(
        "-p",
        "--remote-port",
        action="store",
        type="int",
        dest="port",
        default=default_port,
        help="port on server forward (default: %d)" % default_port,
    )
    parser.add_option(
        "-u",
        "--user",
        action="store",
        type="string",
        dest="user",
        default=getpass.getuser(),
        help="username for SSH authentication (default: %s)" % getpass.getuser(),
    )
    parser.add_option(
        "-k",
        "--key",
        action="store",
        type="string",
        dest="keyfile",
        default=None,
        help="private key file to use for SSH authentication",
    )
    parser.add_option(
        "",
        "--no-key",
        action="store_false",
        dest="look_for_keys",
        default=True,
        help="don't look for or use a private key file",
    )
    parser.add_option(
        "-P",
        "--password",
        action="store_true",
        dest="readpass",
        default=False,
        help="read password (for key or password auth) from stdin",
    )
    parser.add_option(
        "-r",
        "--remote",
        action="store",
        type="string",
        dest="remote",
        default=None,
        metavar="host:port",
        help="remote host and port to forward to",
    )
    option, args = parser.parse_args()
    if len(args) != 1:
        parser.error("Incorrect number of arguments")
    if option.remote is None:
        parser.error("Remote adress required (-r)")

    g_verbose = option.verbose
    server_host, server_port = get_host_port(args[0], SSH_port)
    remote_host, remote_port = get_host_port(option.remote, SSH_port)
    return option, (server_host, server_port), (remote_host, remote_port)

def main():
    option, server, remote = parse_options()

    password = None
    if option.readpass:
        password = getpass.getpass("Enter SSH password:")

    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy())

    verbose("Connecting to ssh host %s : %d ..." % (server[0], server[1]))
    try:
        client.connect(
            server[0],
            server[1],
            username = option.user,
            key_filename = option.keyfile,
            look_for_keys = option.look_for_keys,
            password=password,
        )
    except Exception as e:
        print("*** Failed to connect %s : %d, %r" % (server[0], server[1], e))
        sys.exit(1)

    verbose(
        "Now forwarding remote port %d to %s:%d..." % (option.port, remote[0], remote[1])
    )

    try:
        reverse_forward_tunnel(option.port, remote[0], remote[1], client.get_transport())
    except KeyboardInterrupt:
        print("Ctrl+c; Port forwarding stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()   




    




