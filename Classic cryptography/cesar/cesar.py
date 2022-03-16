ruta = "1.txt"

f = open("1.txt", 'r')
f2 = open("1des.txt", 'w')
mensaje = f.read()
msjDes = ""

offsInicial = 910
k = 22

for l in mensaje:
    if ord(l) >= 127:
        num = ord(l)-offsInicial
        if num < 91 and num > 64:
            letra = chr((num - k)%26 + 65)
            msjDes += letra
        else : msjDes += l
    else : msjDes += l

f2.write(msjDes)
