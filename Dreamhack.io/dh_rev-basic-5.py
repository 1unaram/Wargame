data = [0xAD, 0xD8, 0xCB, 0xCB, 0x9D, 0x97, 0xCB, 0xC4, 0x92, 0xA1, 0xD2,
        0xD7, 0xD2, 0xD6, 0xA8, 0xA5, 0xDC, 0xC7, 0xAD, 0xA3, 0xA1, 0x98, 0x4C, 0x00]


for i in range(32, 126 + 1):
    str = ""
    str += chr(i)
    pre = i

    for j in range(len(data)):
        temp = int(data[j] - pre)
        pre = temp

        if temp > 126 or temp < 32:
            break

        str += chr(temp)

    print(str)

# a1[0] + a[1] == 0xAD
# a1[index + 1]  == byte[index] - a1[index]

# 32_____

# word
# ord0
# 0xAD = 173 / D8 = 216
