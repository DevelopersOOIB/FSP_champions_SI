from random import randint

FLAG = 'flag{?????????????????????????????????????}'

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def isPrime(p):
    if p & 1 == 0:
        return False
    for _ in range(100):
        a = randint(2, p - 2)
        if pow(a, p - 1, p) != 1:
            return False
    return True

def getPrime(len_p):
    p = randint(1 << (len_p - 1), 1 << len_p) | 1
    while not isPrime(p):
        p += 2
    return p

def getKey(len_key):
    p, q = getPrime((len_key >> 1) + 1), getPrime((len_key >> 1) + 1)
    n = p * q
    fi = (p - 1) * (q - 1)
    e1 = randint(3, fi - 1)
    while gcd(e1, fi) != 1:
        e1 = randint(3, fi - 1)
    e2 = randint(3, fi - 1)
    while gcd(e2, fi) != 1:
        e2 = randint(3, fi - 1)
    d1 = pow(e1, -1, fi)
    d2 = pow(e2, -1, fi)
    return (e1, e2, n), (p, q, d1, d2)

def encryptKey(sk, pk):
    p, q, _, _ = sk
    e1, e2, n = pk
    c1 = pow(4*p + 7*q, e1, n)
    c2 = pow(19*p + 3*q, e2, n)
    return c1, c2

def main():
    pk, sk = getKey(2048)
    c1, c2 = encryptKey(sk, pk)
    print(f'n = {pk[2]}\n' + \
          f'e1 = {pk[0]}\n' + \
          f'e2 = {pk[1]}\n' + \
          f'c1 = {c1}\n' + \
          f'c2 = {c2}')
    print('Enter p:')
    p = int(input())
    if p == 1:
        return 0
    print('Enter q:')
    q = int(input())
    if q == 1:
        return 0
    if p*q == pk[2]:
        print(FLAG)
    else:
        print("I didn't guess")
        
if __name__ == "__main__":
    main()
