#Get- request
"""
import urllib.parse
import urllib.request

url = 'https://vk.com'
with urllib.request.urlopen(url) as response:
    content = response.read().decode('utf-8')
    print(content)
"""

#PAST - request
"""
import urllib.request
import urllib.parse
url = 'https://vk.com'

info = {'phone':'79092105955'}
data = urllib.parse.urlencode(info).encode()  #bytes

req = urllib.request.Request(url, data)  #POST
with urllib.request.urlopen(req) as response:
    content = response.read()
    print(content)
"""

#HTTP -request
"""
import requests
url = 'https://vk.com'
response = requests.get(url) #GETss

data = {'phone':'89092105955'}
response = requests.post(url, data=data) #POST
print(response.text) #string
"""

#extract links from HTTP(lxml)
"""
from io import BytesIO
from lxml import etree
import requests

url = 'https://nostarch.com'
r = requests.get(url)

content = r.content #bytes

parser = etree.HTMLParser()
content = etree.parse(BytesIO(content), parser=parser)
for link in content.findall('//a'): #search everething links(elements a)
    print(f'{link.get('href')} -> {link.text}')
"""

#extract links from HTTP(Beatifulsoup)
"""
from bs4 import BeautifulSoup as bs
import requests

url = 'https://nostarch.com'
response = requests.get(url)

tree = bs(response.text, 'html.parser')
for link in tree.find_all('a'):
    print(f"{link.get('href')} -> {link.text}")
"""
















