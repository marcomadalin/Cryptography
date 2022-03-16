fr = open('C:\\Users\madal\PycharmProjects\C\LAB1\cesarCode.txt', 'r', encoding="utf8")
mensaje = fr.read()
msjDes = ""

offsInicial = 9007
k = 14
min = 100000
boo = True
next = input()

while next == "1":
    fw = open('C:\\Users\madal\PycharmProjects\C\LAB1\cesarDecode.txt', 'w', encoding="utf8")
    for l in mensaje:
        if ord(l) >= 127:
            if 9000 < ord(l) < min: min = ord(l)
            num = ord(l)-offsInicial
            if num < 91 and num > 64:
                letra = chr((num - k)%26 + 65)
                msjDes += letra
            else : msjDes += l
        else : msjDes += l
    print(min)
    print(msjDes)
    fw.write(msjDes)
    fw.close()
    print(k)
    k += 1
    next = input()

