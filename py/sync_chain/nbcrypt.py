# nbcrypt.py
# easy-to-use cryptography functions

from ecdsa import SECP256k1, SigningKey, VerifyingKey
from sha3 import sha3_512
import scrypt
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def hash(data):
    if type(data)!=bytes:
        if type(data)!=str:
            raise ValueError("Expected str or bytes")
        data = data.encode()
    return sha3_512(data).digest()

def make_keypair():
    pri = SigningKey.generate(curve=SECP256k1)
    return pri.to_string(), pri.get_verifying_key().to_string()

def sign(data, prikey):
    if type(data)!=bytes:
        if type(data)!=str:
            raise ValueError("Expected str or bytes")
        data = data.encode()
    return SigningKey.from_string(prikey, SECP256k1).sign(data)
def verify(data, pubkey, signature):
    if type(data)!=bytes:
        if type(data)!=str:
            raise ValueError("Expected str or bytes")
        data = data.encode()
    try:
        return VerifyingKey.from_string(pubkey, SECP256k1).verify(signature, data)
    except:
        return False
def encode_key(pri, password="", pub=None):

    if pub==None:
        # determine pub key from pri
        pub = SigningKey.from_string(pri, SECP256k1).get_verifying_key().to_string()
        
    salt = os.urandom(16)
    iv = os.urandom(16)

    hashpass = scrypt.hash(password, salt, N=32768, r=8, p=1, buflen=128)[:32]
    
    backend = default_backend()

    cipher = Cipher(algorithms.AES(hashpass), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    pri_ct = encryptor.update(pri) + encryptor.finalize()
    #           32      16    16    64
    resultat = pri_ct + iv + salt + pub
    return resultat

def decode_key(keydat, password=""):
    pub = keydat[64:]
    iv = keydat[32:48]
    salt = keydat[48:64]
    cyphertext = keydat[:32]

    hashpass = scrypt.hash(password, salt, N=32768, r=8, p=1, buflen=128)[:32]

    backend = default_backend()
    cipher = Cipher(algorithms.AES(hashpass), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    
    pri = decryptor.update(cyphertext) + decryptor.finalize()

    if SigningKey.from_string(pri, SECP256k1).get_verifying_key().to_string()==pub:
        return pri, pub
    else:
        raise Exception("Incorrect Password.")
