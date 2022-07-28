from pwn import *


# Define slog function
def slog(n, m): return success(": ".join([n, hex(m)]))


# Connect
p = process('./ssp_000')

# Set Context
context.arch = 'amd64'
context.endian = 'little'
