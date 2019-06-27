# nbcrypt.py
# easy-to-use cryptography functions

from ecdsa import SECP256k1, SigningKey
from sha3 import sha3_512

def hash(data):
    if type(data)!=bytes:
        if type(data)!=str:
            raise ValueError("Expected str or bytes")
        data = data.encode()
    return sha3_512(data)

def make_keypair():
    pri = SigningKey.generate(curve=SECP256k1)
    return pri.to_string(), pri.get_verifying_key().to_string()

#def sign(data, 
