#! /usr/bin/python3
# by pts@fazekas.hu at Thu May 24 18:44:15 CEST 2018

"""Pure Python 3 implementation of the ChaCha20 stream cipher.
It works with Python 3.5 (and probably also earler Python 3.x).
Based on https://gist.github.com/cathalgarvey/0ce7dbae2aa9e3984adc
Based on Numpy implementation: https://gist.github.com/chiiph/6855750
Based on http://cr.yp.to/chacha.html
More info about ChaCha20: https://en.wikipedia.org/wiki/Salsa20
"""
import binascii
import struct
import collections
import matplotlib.pyplot as plt

def printState(x):
  for i in range(4):
    s = ""
    for j in range(4):
      s += str((hex(x[4*i+j] & 0xffffffff)))
      s += " "
    print(s)

def computeMissmatchingBits(memCount, memPos, org, act):
  count = 0
  for i in range(16):
    borg = str(bin(org[i]))[2:].zfill(32)
    bact = str(bin(act[i]))[2:].zfill(32)
    for j in range(len(borg)):
      if borg[j] != bact[j]:
        count += 1
        val = memPos.get(i*32+j)
        if val is None:
          memPos[i*32+j] = 1
        else:
          memPos[i * 32 + j] = val + 1
  val = memCount.get(count)
  if val is None:
    memCount[count] = 1
  else:
    memCount[count] = val + 1

def getCumulativeFreqs(x):
  y = [x[0]]
  for i in range(1,len(x)):
    y.append(y[i-1]+x[i])
  return y

def yield_chacha20_xor_stream(key, iv, position=0, state=None, quarters=0):
  """Generate the xor stream with the ChaCha20 cipher."""
  if not isinstance(position, int):
    raise TypeError
  if position & ~0xffffffff:
    raise ValueError('Position is not uint32.')
  if not isinstance(key, bytes):
    raise TypeError
  if not isinstance(iv, bytes):
    raise TypeError
  if len(key) != 32:
    raise ValueError
  if len(iv) != 12:
    raise ValueError

  def rotate(v, c):
    return ((v << c) & 0xffffffff) | v >> (32 - c)

  def quarter_round(x, a, b, c, d):
    x[a] = (x[a] + x[b]) & 0xffffffff
    x[d] = rotate(x[d] ^ x[a], 16)
    x[c] = (x[c] + x[d]) & 0xffffffff
    x[b] = rotate(x[b] ^ x[c], 12)
    x[a] = (x[a] + x[b]) & 0xffffffff
    x[d] = rotate(x[d] ^ x[a], 8)
    x[c] = (x[c] + x[d]) & 0xffffffff
    x[b] = rotate(x[b] ^ x[c], 7)

  ctx = [0] * 16
  ctx[:4] = (1634760805, 857760878, 2036477234, 1797285236)
  ctx[4 : 12] = struct.unpack('<8L', key)
  ctx[12] = position
  ctx[13 : 16] = struct.unpack('<LLL', iv)
  state.append(0)
  while 1:
    x = list(ctx)
    for i in range(10):
      if quarters != 1:
        if quarters != 3:
          quarter_round(x, 0, 4,  8, 12)
        quarter_round(x, 1, 5,  9, 13)
        quarter_round(x, 2, 6, 10, 14)
        quarter_round(x, 3, 7, 11, 15)
      if quarters != 2:
        quarter_round(x, 0, 5, 10, 15)
        if quarters != 3:
          quarter_round(x, 1, 6, 11, 12)
        quarter_round(x, 2, 7,  8, 13)
        quarter_round(x, 3, 4,  9, 14)
    y = [(x[i] + ctx[i]) & 0xffffffff for i in range(16)]
    """if position == 1:
      print("INITAL STATE")
      printState(ctx)
      print()
      print("POST QUARTER STATE")
      printState(x)
      print()
      print("POST SUM STATE")
      printState(y)
      print()"""
    state.pop()
    state.extend(y)
    for c in struct.pack('<16L', *((x[i] + ctx[i]) & 0xffffffff for i in range(16))):
      yield c
    ctx[12] = (ctx[12] + 1) & 0xffffffff

def chacha20_encrypt(data, key, iv=None, position=0, state=None, quarters=0):
  """Encrypt (or decrypt) with the ChaCha20 cipher."""
  if not isinstance(data, bytes):
    raise TypeError
  if iv is None:
    iv = b'\0' * 12
  if isinstance(key, bytes):
    if not key:
      raise ValueError('Key is empty.')
    if len(key) < 32:
      key = (key * (32 // len(key) + 1))[:32]
    if len(key) > 32:
      raise ValueError('Key too long.')

  return bytes(a ^ b for a, b in zip(data, yield_chacha20_xor_stream(key, iv, position, state,quarters)))


uh = lambda x: binascii.unhexlify(bytes(x,'ascii'))
ciphertext = '76b8e0ada0f13d90405d6ae55386bd28bdd219b8a08ded1aa836efcc8b770dc7da41597c5157488d7724e03fb8d84a376a43b8f41518a11cc387b6698af700'
key = '000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f'
iv = '000000090000004a00000000'

for j in range(0,4):
  org = []
  res = chacha20_encrypt(b'\0' * len(uh(ciphertext)), uh(key), uh(iv), 1, org,j)
  """print("counter = 1:")
  printState(org)
  print()"""

  memCount = dict()
  memPos = dict()
  for i in range(2,4097):
    act = []
    res = chacha20_encrypt(b'\0' * len(uh(ciphertext)), uh(key), uh(iv), i, act,j)
    """"print("counter = " + str(i) + ":")
    #printState(act)"""
    computeMissmatchingBits(memCount, memPos, org,act)
    """print()"""

  memC = collections.OrderedDict(sorted(memCount.items()))
  memP = collections.OrderedDict(sorted(memPos.items()))

  countKeys = list(memC.keys())
  countVals = list(memC.values())

  countX = list(range(min(countKeys), max(countKeys) + 1))
  countY = [0] * len(countX)
  for i in range(len(countKeys)):
    countY[countKeys[i]-min(countKeys)] = countVals[i]
  countAcY = getCumulativeFreqs(countY)

  posKeys = list(memPos.keys())
  posVals = list(memPos.values())

  posX = list(range(0,512))
  posY = [0] * 512
  for i in range(len(posKeys)):
    posY[posKeys[i]] = posVals[i]
  posAcY = getCumulativeFreqs(posY)

  #Histo bits canviats
  plt.bar(countX, countY,align="center")
  plt.xlim(min(countX)-1, max(countX)+1)
  plt.ylim(-1, max(countY)+1)
  plt.xlabel("nombre de bits canviats")
  plt.ylabel("nombre de vegades canviades")
  plt.show()

  #Freq acumulades bits canviats
  plt.bar(countX, countAcY,align="center")
  plt.xlim(min(countX)-1, max(countX)+1)
  plt.ylim(-1, max(countAcY)+1)
  plt.xlabel("nombre de bits canviats")
  plt.ylabel("nombre de vegades canviades acumulat")
  plt.show()

  #Histo bit i-essim
  plt.bar(posX, posY,align="center")
  plt.xlim(-1, 512)
  plt.ylim(-1, max(posY)+1)
  plt.xlabel("bit i-essim")
  plt.ylabel("nombre de vegades canviades")
  plt.show()

  #Freq acumulades bit i-essim
  plt.bar(posX, posAcY,align="center")
  plt.xlim(-1, 512)
  plt.ylim(-1, max(posAcY)+1)
  plt.xlabel("bit i-essim")
  plt.ylabel("nombre de vegades canviades acumulat")
  plt.show()