from sympy import Matrix, shape

#THEANDINGANDTHEINGTHEOABDOO
fr = open('C:\\Users\madal\PycharmProjects\C\LAB1\hillCode.txt', 'r', encoding="utf8")
textCoded = fr.read()
textDecoded = ""

#calcul de frequencies
freq = dict()
for i in range(len(textCoded)):
    if i+2 < len(textCoded):
        key = textCoded[i] + textCoded[i+1] + textCoded[i+2]
        val = freq.get(key)
        if val is None: freq[key] = 1
        else: freq[key] = val + 1
print(freq)
print()

#obtenim les 3 frequencies maximes
topFreq = dict()
for i in range(3):
    maxKey = ""
    maxVal = 0
    for key in freq:
        if not key in topFreq:
            if freq[key] > maxVal:
                maxKey = key
                maxVal = freq[key]
    topFreq[maxKey] = maxVal
print(topFreq)
print()

#passem caracter a numero
def toNum(c):
    return ord(c) - 65

#passem trigram de caracter a trigram de numero
def trigraphToNum(trig):
    l = list()
    for c in trig: l.append(toNum(c))
    return l

#obtenim els trigrams del diccionari mitjançant clau-valor, el ordre importa perque els agafa del diccionari
#si no surt aqui tambe has de provar amb el ordre del trigrafs
keys = list(topFreq.keys())
t1 = trigraphToNum(keys[0])
t2 = trigraphToNum(keys[1])
t3 = trigraphToNum(keys[2])

#aqui es on hem de provar trigrams, el ordre correspon amb el de dalt, aquí has de provar si no surt
t1o = trigraphToNum("THE")
t2o = trigraphToNum("AND")
t3o = trigraphToNum("ING")

print("THE, Org: " + str(t1o) + " Cod: " + str(t1))
print("AND, Org: " + str(t2o) + " Cod: " + str(t2))
print("ING, Org: " + str(t3o) + " Cod: " + str(t3))
print()

#construim les matrius
M = Matrix([t1o,t2o,t3o])
res1 = Matrix([t1[0],t2[0],t3[0]])
res2 = Matrix([t1[1],t2[1],t3[1]])
res3 = Matrix([t1[2],t2[2],t3[2]])
print(M)
print()
print(res1)
print(res2)
print(res3)
print()

def toValue(x):
    return x[0]
#resolem els sistemes per obtenir la matriu original i calculem la seva inversa mod 26
Minv = Matrix.inv_mod(M,26)
Mo = Matrix([list(map(toValue,(Minv*res1).tolist())),list(map(toValue,(Minv*res2).tolist())),list(map(toValue,(Minv*res3).tolist()))])
Moinv = Matrix.inv_mod(Mo,26)

#passem el text original a numeros
textCodedNum = list(map(toNum,textCoded))

#decodifquem trigram
def decodeTrigraph(tri,mat):
    org = mat * Matrix(tri)
    decodedText = ""
    for i in range(len(org)):
        org[i] = int(round(org[i])) % 26
        decodedText += chr(65 + org[i])
    return decodedText

#AIXO ES NOMES UN JOC DE PROVES
textEx = "THEANDINGANDTHEINGTHEOABDOO"
textEx = list(map(toNum,textEx))
textDecEx = ""

i = 0
while i < len(textEx):
    textDecEx += decodeTrigraph(textEx[i:i+3],Mo)
    i += 3

print("TEXT EXEMPLE CODIFICAT = " + textDecEx)
print("TEXT EXEMPLE RESULTAT =  HIHAKNCPAAKNHIHCPAHIHKNNPBB")
print()
#ACABA EL JOC DE PROVES

i = 0
while i < len(textCodedNum):
    textDecoded += decodeTrigraph(textCodedNum[i:i+3],Moinv)
    i += 3

fw = open('C:\\Users\madal\PycharmProjects\C\LAB1\hillDecode.txt', 'w', encoding="utf8")
fw.write(textDecoded)
fw.close()
print("TEXT ORIGINAL = " + textDecoded)
