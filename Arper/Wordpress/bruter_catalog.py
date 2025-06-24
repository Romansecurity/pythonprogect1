import queue
import requests
import threading 
import sys
from termcolor import colored, cprint

AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0'
EXTENSIONS = ['.php', '.bak', '.orig', '.inc']
TARGET = 'http://www.tkdvrn.ru'
THREADS = 5
WORDLIST = '/home/roman/Downloads/SVNDigger/papka/all.txt'

def get_words(resume=None): # return queue with words
    def extend_words(word):
        if "." in word:
            words.put(f'/{word}') #adding a word to the URL
        else:
            words.put(f'/{word}/') #read as folder name
        
        for extension in EXTENSIONS:
            words.put(f'/{word}{extension}')

    with open(WORDLIST) as f:
        raw_words = f.read()

    found_resume = False
    words = queue.Queue()
    for word in raw_words.split():
        if resume is not None:
            if found_resume:
                extend_words(word)
            elif word == resume:
                found_resume = True
                print(f'Resuming wordlist from: {resume}')
        else:
            print(word)
            extend_words(word)
    return words

def dir_bruter(words):  #important function 
    headers = {'User-Agent': AGENT}
    while not words.empty():
        url = f'{TARGET}{words.get()}'
        try:
            r = requests.get(url, headers=headers)
        except requests.exceptions.ConnectionError:
            sys.stderr.write('x')
            sys.stderr.flush()
            continue

        if r.status_code == 200:
            cprint(f'\n Succes ({r.status_code}: {url})', 'green')
        elif r.status_code == 404:
            sys.stderr.write('.')
            sys.stderr.flush()
        else:
            cprint(f'{r.status_code} => {url}', 'blue')

if __name__ == '__main__':
    words = get_words()
    print('Press Enter to continue')
    sys.stdin.readline()
    for _ in range(THREADS):
        t = threading.Thread(target=dir_bruter, args=(words,))
        t.start()





    





