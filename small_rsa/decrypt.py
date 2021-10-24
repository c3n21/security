from itertools import count
import sys
import math
from types import GeneratorType, GenericAlias
from typing import Optional, Tuple

def gen_primes():
    """ Generate an infinite sequence of prime numbers.
    """
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    #
    D = {}
    
    # The running integer that's checked for primeness
    q = 2
    
    while True:
        if q not in D:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            # 
            yield q
            D[q * q] = [q]
        else:
            # q is composite. D[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next 
            # multiples of its witnesses to prepare for larger
            # numbers
            # 
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
        
        q += 1

def generate_keypair_from(n: int, e: int):

    gen1 = gen_primes()
    gen2 = gen_primes()
    for p in gen1:
        for q in gen2:
            if p*q == n:
                to = (p - 1)*(q - 1)
                if to > e:
                    d = 0
                    while e*d % n != 1:
                        d += 1

                    yield d

def decrypt(c: int, d: int, n: int) -> int:
    return int(math.pow(c, d)) % n

if __name__ == '__main__':
    n = ""
    e = ""
    c = ""
    with(open("rsa.txt") as f):
        for line in f:
            if line.startswith("n"):
                n = line.split("=")[1]
            if line.startswith("e"):
                e = line.split("=")[1]
            if line.startswith("c"):
                c = line.split("=")[1]

    n = int(n)
    e = int(e)
    c = int(c)
    print(f"n = {n}")
    print(f"e = {e}")
    print(f"c = {c}")

    for d in count(start=0, step=1):
        print("Decrypting")
        decrypted = decrypt(c, d, n)
        b = decrypted.to_bytes(100, sys.byteorder)
        try:
            s = b.decode("utf-8")
            if "spflg" in s:
                print(f"text = {s}")
            else:
                print(f"text = {s}")
        except UnicodeDecodeError:
            pass

    
