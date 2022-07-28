from pwn import *

HOST = 'host3.dreamhack.games'
PORT = 18429
p = remote(HOST, PORT)

# p = process('./r2s')


str = p.recvline()
buf_addr = str[-15:-1]
print(f'[+] Address of buf: {buf_addr}')

str = p.recvline()
distance = str[-3:-1]
print(int(distance.decode('utf-8'), 16))