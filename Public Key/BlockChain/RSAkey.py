from Crypto import Random
from Crypto.Util import number
import math
import sympy
from hashlib import sha256
from time import time

class rsa_key:
    def __init__(self,bits_modulo=2048,e=2**16+1):
        '''
        genera una clau RSA (de 2048 bits i amb exponent p´ublic 2**16+1 per defecte)
        '''
        self.publicExponent = e
        self.primeP, self.primeQ = self.generatePrimePQ(e, bits_modulo)
        self.modulus = self.primeP*self.primeQ
        self.privateExponent = sympy.mod_inverse(self.publicExponent, (self.primeP - 1) * (self.primeQ - 1))
        if (self.privateExponent < 0): self.privateExponent = self.privateExponent*(-1)
        self.privateExponentModulusPhiP = self.privateExponent%(self.primeP-1)
        self.privateExponentModulusPhiQ = self.privateExponent%(self.primeQ-1)
        self.inverseQModulusP = sympy.mod_inverse(self.primeQ, self.primeP)

    def generatePrimePQ(self, e, bits_modulo):
        p = number.getPrime(bits_modulo, randfunc=Random.get_random_bytes)
        q = number.getPrime(bits_modulo, randfunc=Random.get_random_bytes)
        correct = (p != q) & (math.gcd(e, (p-1)*(q-1)) == 1)
        while (not correct):
            p = number.getPrime(bits_modulo, randfunc=Random.get_random_bytes)
            q = number.getPrime(bits_modulo, randfunc=Random.get_random_bytes)
            correct = (p != q) & (math.gcd(e, (p-1)*(q-1)) == 1)
        return p,q

    def sign(self,message):
        '''
        retorma un enter que ´es la signatura de "message" feta amb la clau RSA fent servir el TXR
        '''
        a = pow(message,self.privateExponentModulusPhiP,self.primeP)
        b = pow(message,self.privateExponentModulusPhiQ,self.primeQ)
        return a*self.inverseQModulusP*self.primeQ + b*(1-self.inverseQModulusP*self.primeQ) #s


    def sign_slow(self,message):
        '''
        retorma un enter que ´es la signatura de "message" feta amb la clau RSA sense fer servir el TXR
        '''
        return pow(message,self.privateExponent, self.modulus)

    def print(self, m):
        print("P = ", self.primeP)
        print("Q = ", self.primeQ)
        print("P==Q? ", (math.gcd(self.publicExponent, (self.primeP-1)*(self.primeQ-1))))



class rsa_public_key:
    def __init__(self, rsa_key):
        '''
        genera la clau publica RSA asociada a la clau RSA "rsa_key"
        '''
        self.publicExponent = rsa_key.publicExponent
        self.modulus = rsa_key.modulus

    def verify(self, message, signature):
        '''
        retorna el boole`a True si "signature" es correspon amb una
        signatura de "message" feta amb la clau RSA associada a la clau
        publica RSA.
        En qualsevol altre cas retorma el boole`a False
        '''
        return (pow(signature, self.publicExponent, self.modulus) == message)


if __name__ == "__main__":

    RSA = rsa_key(bits_modulo=4096)
    m = 123457873590347
    RSA.print(m)
    s = RSA.sign(m)
    public = rsa_public_key(RSA)
    print(public.verify(m,s))

"""

if __name__ == "__main__":

    bits_modulo = [512, 1024, 2048, 4096]
    messages = [i for i in range(100)]

    output_string = "Bits Modulo,Tiempo con TXR,Tiempo sin TXR\n"

    for modulo in bits_modulo:
        RSA = rsa_key(bits_modulo=modulo)

        now = time()
        for message in messages:
            RSA.sign(message)
        time_signatures = time() - now

        now = time()
        for message in messages:
            RSA.sign_slow(message)
        slow_time_signatures = time() - now

        output_string += f"{modulo},{time_signatures},{slow_time_signatures}\n"

        print(f'''
        module: {modulo}
        fast: {time_signatures}
        slow: {slow_time_signatures}
        ''')

    with open("output/tabla_comparativa.csv", "w") as output_file:
        output_file.write(output_string)
"""
