from math import *

fr = open('2.txt', 'r', encoding="utf8")
ff = open('2Des.txt', 'w', encoding="utf8")
textOrg = fr.read()
next = input()
r = 115

while next == "1":
    textNew = ""
    c = ceil(len(textOrg)/r)
    for i in range(0,r):
        for j in range(0,c):
            if (i+j*r < len(textOrg)): textNew += textOrg[i+j*r]
    print(textNew)
    print("k = " + str(r))
    next = input()
    r += 1

textNew = ""
r = 164
c = ceil(len(textOrg)/r)
for i in range(0,r):
    for j in range(0,c):
        if (i+j*r < len(textOrg)): textNew += textOrg[i+j*r]
ff.write(textNew)
