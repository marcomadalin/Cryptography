from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import magic
import hashlib
import filetype
from os import remove

ELEM = ''.join([chr(i) for i in range(0,127)])
BS = AES.block_size

def keyGenerator():
    posKeys = []
    for k1 in ELEM:
        for k8 in ELEM:
            posKeys.append(f"{k1 * 8}{k8 * 8}")
    return posKeys

def open_file(path, ext):
    with open(f"{path}.{ext}", 'rb') as f:
        return f.read()

def save_file(path, data):
    with open(path, "wb") as f:
        f.write(data)
    print(f"Successful completion: {path} has been created")

class AESdecryptor:

    def __init__(self, msg):
        self.enc = msg

    def decrypt(self, mode, key, iv):
        cipher = AES.new(key, mode, iv)
        #return cipher.decrypt(self.enc)
        return unpad(cipher.decrypt(self.enc), BS, 'pkcs7')


if __name__ == "__main__":

    file = '2021_09_30_10_53_46_marco.madalin.farcas.puerta_trasera'
    bin_msg = open_file(path=("files/"+file), ext="enc")
    decryptor = AESdecryptor(bin_msg)
    posKeys = keyGenerator()
    count = 0
    for k in posKeys:
        try:
            h = hashlib.sha256(k.encode()).digest()
            iv = h[16:]
            key = h[:16]
            decrypted = decryptor.decrypt(AES.MODE_CBC, key, iv)
            #if decrypted[-2] == decrypted[-1]:
            count += 1
            if (count%10 == 0): print(count)
            #print(decrypted[-1], decrypted[-2])
            save_file("results/d"+str(count), decrypted)
            kind = filetype.guess("results/d"+str(count))
            if not(kind is None):
                print('File extension: %s' % kind.extension)
                print('File MIME type: %s' % kind.mime)
                print('++++++++++++++++++++')
            else :
                pass
                #print('Cannot guess file type!')
                #print(magic.from_file("results/d"+str(count)))
         #print('###################################################')
        except ValueError:
            pass

    print(count)
