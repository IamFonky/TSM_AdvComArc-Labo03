# This whole file has been made using Diego Vilagrassa's code and advices.

import hashlib
import base64
from Crypto.Cipher import AES
from Crypto import Random


def padMessage(s):
    return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)

def unpadMessage(s):
    return s[:-ord(s[len(s)-1:])]

# Uses aes-256-cbc encryption
def encrypt(message, key):
    message = padMessage(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(message.encode()))

# Uses aes-256-cbc decryption
def decrypt(ciphertext, key):
    enc = base64.b64decode(ciphertext)
    iv = enc[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpadMessage(cipher.decrypt(enc[AES.block_size:]))

# Derive a key from a point on the curve
def derivateKey(x, y):
    # Convert x and y coordinates to bytes
    x_bytes = x.to_bytes((x.bit_length() + 7) // 8, byteorder='big')
    y_bytes = y.to_bytes((y.bit_length() + 7) // 8, byteorder='big')

    # Concatenate x and y bytes
    xy_bytes = x_bytes + y_bytes

    # Hash the concatenated bytes using SHA256
    hash_obj = hashlib.sha256(xy_bytes)
    key = hash_obj.digest()

    return key

# https://cryptobook.nakov.com/asymmetric-key-ciphers/ecdh-key-exchange-examples
def compress(pubKey):
    return hex(pubKey.x) + hex(pubKey.y % 2)[2:]
