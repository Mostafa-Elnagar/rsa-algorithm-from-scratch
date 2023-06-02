from generate_random_prime import gen_unique_primes
import random
from parallel_d_gen import gen_private

def exp_mod(a, b, n):
    c, f = 0, 1
    b = "{0:b}".format(b)
    for i in b:
        c *= 2
        f = (f ** 2) % n
        if int(i) == 1:
            c += 1
            f = (f * a) % n
    return f

def begcd(a, b):
    """ Binary Extended gcd """
    if b == 0:
        return a, 1, 0

    last_x, last_y = 1, 0
    x, y = 0, 1

    while b != 0:
        quotient = a // b
        a, b = b, a % b
        x, last_x = last_x - quotient * x, x
        y, last_y = last_y - quotient * y, y

    return a, last_x, last_y

def gcd(a, b):
    return begcd(a, b)[0]

def find_modular_inverse(a, m):
    gcd, x, _ = begcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist.")

    return x % m

def gen_keys(nbits):
    p, q = gen_unique_primes(2, nbits)
    n = p * q
    phi = (p - 1) * (q - 1)

    # Generate Public Key
    e = 2
    while e < phi:
        if (gcd(phi, e) == 1):
            break
        e += 1
    print("Public key have been generated")

    # Generate Private Key 
    d = find_modular_inverse(e, phi)
        
    print("Private Key have been generated")
    return (e, n), (d, n)
    
def encrypt(msg, pub_key):
    e, n = pub_key
    c = [pow(ord(c), e, n) for c in msg]
    return c 

def decrypt(cipher, priv_key):
    d, n = priv_key
    msg = "".join([chr(pow(int(c), d, n)) for c in cipher])
    return msg 

def factorization(n):

    factors = []

    def get_factor(n):
        x_fixed = 2
        cycle_size = 2
        x = 2
        factor = 1

        while factor == 1:
            for _ in range(cycle_size):
                if factor > 1: 
                    break
                x = (x * x + 1) % n
                factor = gcd(x - x_fixed, n)

            cycle_size *= 2
            x_fixed = x

        return factor

    while n > 1:
        next = get_factor(n)
        factors.append(next)
        n //= next

    return factors

def pack(to_pac):
    s = [str(item) for item in to_pac]
    return ",".join(s)

def unpack(s):
    return list(map(int, s.split(",")))

if __name__ == "__main__":
    for nbits in range(4, 16):
        
        print(f"nbits={nbits}")
        pub_key, priv_key = gen_keys(nbits)
        print(f"e={pub_key[0]}")
        print(f"d={priv_key[0]}")
        print(f"n={priv_key[1]}")

        for k in range(1, nbits):
            msg = (2 ** nbits - 1) * k
            encrypted = encrypt(msg, pub_key)
            decrypted = decrypt(encrypted, priv_key)
            if msg != decrypted:
                print(f"k={k}")
                print(f"msg: {msg}")
                print(f"encrypted: {encrypted}")
                print(f"decrypted: {decrypted}")

        print("_"*20)