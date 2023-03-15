import requests
from bs4 import BeautifulSoup as bs

Host = 'https://webhacking.kr/challenge/bonus-14/'

str = ''
for i in range(39):
    res = requests.get(f'{Host}?m={i}')
    soup = bs(res.text, "html.parser")
    print(soup.select_one('#aview'))

print(str)

res = requests.get(f'{Host}/?m=1')
print(res.content)