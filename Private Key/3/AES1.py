import base64
from Crypto.Cipher import AES
import magic

BS = AES.block_size

def open_file(path, ext):
    with open(f"{path}.{ext}", 'rb') as f:
        return f.read()

def save_file(path, data):
    with open(path, "wb") as f:
        f.write(data)
    print(f"Successful completion: {path} has been created")

class AESdecryptor:

    def __init__(self, key):
        self.key = key

    def decrypt(self, enc, mode):
        iv = enc[:16]
        #print(iv)
        cipher = AES.new(self.key, mode, iv)
        return cipher.decrypt(enc[16:])
        #return unpad(cipher.decrypt(enc[16:]), BS, 'pkcs7')


if __name__ == "__main__":

    file = '2021_09_30_10_53_46_marco.madalin.farcas'

    bin_key = open_file(path=("files/"+file), ext="key")
    #print(bin_key)
    decryptor = AESdecryptor(bin_key)

    bin_msg = open_file(path=("files/"+file), ext="enc")
    decryptedMsg = decryptor.decrypt(bin_msg, AES.MODE_CFB)
    save_file("results/decrypted_madalin.jpg", decryptedMsg)
    #print(magic.from_file('results/decrypted_gera'))
