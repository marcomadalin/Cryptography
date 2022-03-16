
import pickle
from time import time
from random import randint
from hashlib import sha256

from RSAkey import rsa_key
from transaction import transaction

class block:
    def __init__(self):
        '''
        crea un bloc (no neces`ariamnet v`alid)
        '''
        self.block_hash = None
        self.previous_block_hash = None
        self.transaction = None
        self.seed = None
    def genesis(self,transaction):
        '''
        genera el primer bloc d’una cadena amb la transacci´o "transaction" que es caracteritza per:
        - previous_block_hash=0
        - ser valid
        '''
        self.previous_block_hash = 0
        self.transaction = transaction
        self.block_hash = generateHash(self,16,False)
        return self

    def next_block(self, transaction):
        '''
        genera el seg¨uent block v`alid amb la transacci´o "transaction"
        '''
        b = block()
        b.previous_block_hash = self.block_hash
        b.transaction = transaction
        b.block_hash = generateHash(b,16,False)
        return b

    def next_wrong_block(self, transaction):
        """
        Genera el següent bloc invàlid amb la transacció "transaction".
        """
        b = block()
        b.transaction = transaction
        b.previous_block_hash = self.block_hash
        b.block_hash = generateHash(b,16,True)
        return b

    def verify_block(self):
        '''
        Verifica si un bloc ´es v`alid:
        -Comprova que el hash del bloc anterior cumpleix las condicions exigides
        -Comprova la transacci´o del bloc ´es v`alida
        -Comprova que el hash del bloc cumpleix las condicions exigides
        Si totes les comprovacions s´on correctes retorna el boole`a True.
        En qualsevol altre cas retorma el boole`a False
        '''
        previous = self.previous_block_hash < 2**(256 - 16)
        trans = self.transaction.verify()
        selfb = self.block_hash < 2**(256 - 16)
        return previous and trans and selfb and self.verifyHashSeed()

    def verifyHashSeed(self):
        entrada = str(self.previous_block_hash)
        entrada = entrada + str(self.transaction.public_key.publicExponent)
        entrada = entrada + str(self.transaction.public_key.modulus)
        entrada = entrada + str(self.transaction.message)
        entrada = entrada + str(self.transaction.signature)
        entrada = entrada + str(self.seed)
        h = int(sha256(entrada.encode()).hexdigest(), 16)
        return h == self.block_hash

    def __repr__(self):
        return f"seed = {self.seed}\nprevHash = {self.previous_block_hash}\nhash = {self.block_hash}\nlimit = {2 ** 256 - D}\ntransaccion = {self.transaction}\n"

def generateHash(block, d = 16, wrong = False):
    while True:
        block.seed = randint(0, 2**256)
        entrada=str(block.previous_block_hash)
        entrada+=str(block.transaction.public_key.publicExponent)
        entrada+=str(block.transaction.public_key.modulus)
        entrada+=str(block.transaction.message)
        entrada+=str(block.transaction.signature)
        entrada+=str(block.seed)
        h=int(sha256(entrada.encode()).hexdigest(),16)
        if wrong:
            if h >= 2**(256 - d): break
        else:
            if h < 2**(256 - d): break
    return h
def isGenesis(block):
    return block.previous_block_hash == 0

class block_chain:
    def __init__(self,transaction):
        '''
        genera una cadena de blocs que ´es una llista de blocs,
        el primer bloc ´es un bloc "genesis" generat amb la transacci´o "transaction"
        '''
        b0 = block()
        b0.genesis(transaction)
        self.list_of_blocks = [b0]

    def add_block(self,transaction):
        '''
        afegeix a la llista de blocs un nou bloc v`alid generat amb la transacci´o "transaction"
        '''
        last = self.list_of_blocks[-1]
        next = last.next_block(transaction)
        self.list_of_blocks.append(next)

    def add_wrong_block(self, transaction):
        """
        Afegeix a la llista de blocs un now bloc invàlid generat amb la transacció "transaction".
        """
        next_block = self.list_of_blocks[-1].next_wrong_block(transaction)
        self.list_of_blocks.append(next_block)
        return self

    def verify(self):
        '''
        verifica si la cadena de blocs ´es v`alida:
        - Comprova que tots el blocs s´on v`alids
        - Comprova que el primer bloc ´es un bloc "genesis"
        - Comprova que per cada bloc de la cadena el seg¨uent ´es el correcte
        Si totes les comprovacions s´on correctes retorna el boole`a True.
        En qualsevol altre cas retorma el boole`a False i fins a quin bloc la cadena ´es v´alida
        '''
        #devuelvo el indice del primer blocke erroneo
        for i in range(len(self.list_of_blocks)):
            if i == 0:
                if (not isGenesis(self.list_of_blocks[i])):
                    return False, i
            else:
                if (self.list_of_blocks[i].previous_block_hash != self.list_of_blocks[i-1].block_hash):
                    return False, i
            if (not self.list_of_blocks[i].verify_block()):
                return False, i
        return True, -1



def generateBlockChain(file_name, limit):
    print("loading new blockChain...")
    t0 = time()
    RSA = rsa_key()
    transactionSet = map(lambda i: int(sha256(f"{i}".encode()).hexdigest(), 16), range(100))
    blockchain = block_chain(transaction(next(transactionSet), RSA))

    for i in range(1,100):
        print("loading block number: ", str(i))
        RSA = rsa_key()
        if limit != 100 and i > limit:
            blockchain.add_wrong_block(transaction(next(transactionSet), RSA))
        else:
            blockchain.add_block(transaction(next(transactionSet), RSA))
    t1 = time()

    with open(file_name, 'wb') as output_file:
        pickle.dump(blockchain, output_file)

    print(f"File '{file_name}' has been created succesfully!\nVerification: {blockchain.verify()}\nTime elapsed: {t1 - t0}")

if __name__ == "__main__":
    D = 16
    generateBlockChain("output/MarcoBlocks.pickle", 33)
    generateBlockChain("output/GerardBlocks.pickle", 64)
    generateBlockChain("output/100Blocks.pickle", 100)
