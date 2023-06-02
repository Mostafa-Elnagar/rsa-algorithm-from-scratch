import random 

random.seed(42)

PRIME_LIST = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
    31, 37, 41, 43, 47, 53, 59, 61, 67,
    71, 73, 79, 83, 89, 97, 101, 103,
    107, 109, 113, 127, 131, 137, 139,
    149, 151, 157, 163, 167, 173, 179,
    181, 191, 193, 197, 199, 211, 223,
    227, 229, 233, 239, 241, 251, 257,
    263, 269, 271, 277, 281, 283, 293,
    307, 311, 313, 317, 331, 337, 347, 349
]



def _get_cand_prime(n):
    """
    generate candidate prime
    """

    def pick_rand(n):
        """
        return a random odd number of length n and leading bit = 1 
        """
        n -= 1
        # ensure we get large numbers
        lower = 2 ** (n - 1) + 1
        upper = 2 ** (n) - 1
        if n < 6:
            lower = 3
            
        # to ensure the generated number is odd 
        cand = (random.randrange(lower, upper) << 1) + 1

        return cand

   
    # Repeat until a number satisfying
    while True: 
        # get random number
        p = pick_rand(n)
   
        for d in PRIME_LIST: 
            if (p % d == 0 and d**2 <= p):
                break
            # If no divisor found, return value
            return p
        

def _is_miller_passed(cand_num, n_rabin_trails=25):
    '''Run 25 iterations of Rabin Miller Primality test'''

    def trail_composite(round_tester):
        if pow(round_tester, even_comp, cand_num) == 1:
            return False
        for i in range(max_div_by):
            if pow(round_tester, 2**i * even_comp, cand_num) == cand_num - 1:
                return False
        return True

    max_div_by = 0
    even_comp = cand_num - 1
   
    while even_comp % 2 == 0:
        even_comp >>= 1
        max_div_by += 1
   

    for _ in range(n_rabin_trails):
        round_tester = random.randrange(2, cand_num)
        if trail_composite(round_tester):
            return False
        
    return True

def gen_prime(nbits=512):
    while True:
        prime_candidate = _get_cand_prime(nbits)
        if not _is_miller_passed(prime_candidate):
            continue
        else:
            return prime_candidate

def gen_unique_primes(n=2, nbits=512, iters=1000):
    primes = []
    for i in range(n):
        prime = gen_prime(nbits)
        while prime in primes:
            prime = gen_prime(nbits)
            iters -= 1
            if not iters:
                raise ValueError(f"Can't find more than {i} unique primes with length {nbits} bits.")
        primes.append(prime)
        
    return primes

if __name__ == "__main__":
    n = gen_prime(16)
    p, q = gen_unique_primes(2, 16)
    print(f"p={p}, q={q}")
    print(n)

