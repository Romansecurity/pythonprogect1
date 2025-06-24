import pyfiglet    # text -> ASCII art
from termcolor import cprint

text = 'GOPIENKO 2.0'
ASCII = pyfiglet.figlet_format(text, font='slant')
cprint(ASCII, 'green')



       