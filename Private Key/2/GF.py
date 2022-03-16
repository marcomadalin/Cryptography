import numpy as np
import time

def GF_product_p(a, b):
    if a == 0 or b == 0: return 0

    num = np.binary_repr(b)
    partialRes = [0] * len(num)
    partialRes[0] = a

    grade = len(num) - 1
    result = a

    for i in range(1, len(num)):
        bit7 = np.binary_repr(result, 8)[0]
        result = np.uint8(result << 1)

        if bit7 == '1': result = result ^ 0x1D
        partialRes[i] = result

    for i, bit in enumerate(num[1:], 1):
        if bit == '1': result = result ^ partialRes[grade - i]

    return result


def GF_es_generador(g):
    acc = 1
    for i in range(1, 256):
        acc = GF_product_p(acc, g)
        if acc == 1:
            return i == 255
    return False


def GF_tables():
    g = 2
    acc = g
    exp = [1] * 256
    exp[1] = g
    log = [0] * 256
    log[g] = 1
    for i in range(2, 256):
        acc = GF_product_p(acc, g)
        exp[i] = acc
        log[acc] = i

    return exp, log

exp, log = GF_tables()

def GF_product_t(a, b):
    if a == 0 or b == 0:
        return 0

    index = (log[a] + log[b]) % 255
    prod = exp[index]
    return prod

def GF_invers(a):
    if a == 0: return 0
    return exp[255 - log[a]]

assert GF_invers(0) == 0
assert not GF_es_generador(0)

for i in range(256):
    for j in range(256):
        assert GF_product_p(i, j) == GF_product_t(i, j)
        assert GF_product_p(i, j) == GF_product_p(j, i)
    if i > 0: assert GF_product_p(i, GF_invers(i)) == 1

print('TESTS PASSED')
print()

a = 0xC6
l = [0x2B, 0x02, 0x03, 0x09, 0x0B, 0x0D, 0x0E]
n = 50000
for b in l:
    totalTimeP = 0
    totalTimeT = 0
    timeP = 0
    timeT = 0
    for i in range(n):
        initTimeP = time.time_ns()
        GF_product_p(a, b)
        timeP += (time.time_ns() - initTimeP)

        initTimeT = time.time_ns()
        GF_product_t(a, b)
        timeT += (time.time_ns() - initTimeT)
    totalTimeP = timeP / n
    totalTimeT = timeT / n
    print("Time GF_product_p(" + str(a) + "," + str(b) + ") = " + str(totalTimeP))
    print("Time GF_product_t(" + str(a) + "," + str(b) + ") = " + str(totalTimeT))
    print()
