from RSAkey import rsa_key
from RSAkey import rsa_public_key

class transaction:
    def __init__(self, message, RSAkey):
        '''
        genera una transacci´o signant "message" amb la clau "RSAkey"
        '''
        self.public_key = rsa_public_key(RSAkey)
        self.message = message
        self.signature = RSAkey.sign(message)
    def verify(self):
        '''
        retorna el boole`a True si "signature" es correspon amb una
        signatura de "message" feta amb la clau p´ublica "public_key".
        En qualsevol altre cas retorma el boole`a False
        '''
        return self.public_key.verify(self.message ,self.signature)
