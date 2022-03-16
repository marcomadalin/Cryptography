
from glob import glob
import os
import pickle
from blockchain import block
from blockchain import block_chain
from RSAkey import rsa_key
from RSAkey import rsa_public_key
from transaction import transaction

if __name__ == '__main__':
    file_list = [fn for fn in glob(os.path.join('output/', '*.pickle'))]
    for idx, file_name in enumerate(file_list):
        with open(file_name, 'rb') as file:
            blk = pickle.load(file)
            file.close()

        print(file_name, ' ', blk.verify())

    with open('Tests/files/claveRSA', 'rb') as file:
        RSA = pickle.load(file)
        file.close()

    message = 12321351234123412352346234
    signature = RSA.sign(message)
    print(f'Clave RSA {rsa_public_key(RSA).verify(message, signature)}')
