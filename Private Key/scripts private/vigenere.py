az = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def getIndex(letter):
    return az.index(letter)

def toNumbers(msg):
    M = []
    for x in msg:
        M.append(getIndex(x))
    return M

def toLetter(R):
    r = ""
    for i in R:
        r += az[i]
    return r

msg = "MIMAMAMEMIMAMUCHO"
key = "LAVADAS"

M = toNumbers(msg)
K = toNumbers(key)

R = []
i = 0
j = 0
while (i<len(M)):
    R.append((M[i]+K[j])%26)
    i+=1
    j+=1
    if (j >= len(K)): j = 0
print(toLetter(R))
