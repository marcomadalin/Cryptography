msgSize = 16052
bits = msgSize*8 + 128

while ( bits%128 != 0):
    bits += 8

print(bits/8)
