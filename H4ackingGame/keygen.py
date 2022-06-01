# Buf2[i] == ((Buf1[i] ^ 0x11) ^ 0x1B) - 3

Buf2 = '?;FJDnv8dw8lRulyRmmt'

for i in range(0, 20):
    char = ord(Buf2[i])
    char += 3
    char ^= 0x1B
    char ^= 0x11
    print(chr(char), end="")
