import argparse
import bruteforce 
from termcolor import cprint
import pyfiglet

text = 'GOPIENKO SHADOW'
ASCII = pyfiglet.figlet_format(text, font='slant')
cprint(ASCII, 'magenta')

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--user', help='username')
parser.add_argument('-L', '--users', help='Users file')
parser.add_argument('-p', '--password', help='password')
parser.add_argument('-o', '--passwords', help='Passwords file')
parser.add_argument('-u', '--url', help='URL')
parser.add_argument('-v', '--verbose', help='continious btute force after valid password is found')
parser.add_argument('-d', '--droplet', help='Get droplet info', action='store_true') #flag - True

args = parser.parse_args()

def help_message():
    print('usage: bruteforce.py -l admin -o cain.txt -u http://localhost/wordpress/wp-login.php')

if args.url:
    url = args.url
else:
    help_message()
    exit()

if args.user:
    user = args.user
elif args.users:
    users = args.users
else:
    help_message()
    exit()

if args.password:
    password = args.password
elif args.passwords:
    passwords = args.passwords
else:
    help_message()
    exit()

if args.verbose:
    verbose = True
else:
    verbose = False

if __name__  == '__main__':
    bruteforce.brute_force_passwords(user, passwords, url, verbose)

