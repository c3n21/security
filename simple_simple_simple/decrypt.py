from typing import Tuple
import sys
import math
from itertools import cycle

bits = 16

def encrypt_xor(text: str, key: bytes) -> str:
    """
    Encrypts `text` with using `key`.
    The result is a binary string
    """
    encoded = text.encode("utf-8")
    encrypted = b""
    for t, k in zip(encoded, cycle(key)):
        xored = t ^ k
        xored = xored.to_bytes(1, sys.byteorder)
        encrypted += xored
        #encrypted = encrypted.join((t ^ k).to_bytes(len(key), sys.byteorder).decode("utf-8"))

    return encrypted.decode("utf-8")

def decrypt_xor(encrypted_text: str, n_bytes: int, stop: str) -> str:
    encoded = encrypted_text.encode("utf-8")
    decrypted = b""
    for key in range(0,int(math.pow(2,n_bytes*8))):
        decrypted = b""
        e_key = key.to_bytes(n_bytes, sys.byteorder)
        for t, k in zip(encoded, cycle(e_key)):
            xored = t ^ k
            decrypted += xored.to_bytes(1, sys.byteorder)

        decrypted = str(decrypted)

        if stop in decrypted:
            return decrypted

    return str(decrypted)

if __name__ == '__main__':
    for filename in sys.argv[1:]:
        print(f"Processing '{filename}'")
        
#        encrypted = encrypt_xor("ciao", "p".encode("utf-8"))
#        print(f"encrypted = '{encrypted}'")
#        decrypted = decrypt_xor(encrypted, len("p".encode("utf-8")),"ciao")
#        print(f"decrypted = '{decrypted}'")

        with(open(filename, "r") as file):
            result = decrypt_xor(file.read(), 2, "flag")
            print(f"result = {result}")
   #     p = xor(filename, bits, "flag")
   #     print(p)

