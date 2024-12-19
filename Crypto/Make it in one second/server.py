from random import getrandbits
from time import time

flag = 'flag{????????????????????}'

S = [[12,4,6,2,10,5,11,9,14,8,13,7,0,3,15,1], [6,8,2,3,9,10,5,12,1,14,4,7,11,13,0,15]]

def t(a):
    R = 0
    for i in range(2):
        R <<= 4
        R ^= S[i][a & 0xf]
        a >>= 4
    return R

def roll(a):
    return ((a << 5) | (a >> 3)) & 0xff

def g(a, k):
    return roll(t((a + k) & 0xff))

def get_keys(k):
    K = [0] * 4
    for i in range(4):
        K[i] = k & 0xff
        k >>= 8
    return K

def encrypt(m, k):
    K = get_keys(k)
    L, R = m >> 8, m & 0xff
    for i in range(3):
        L, R = R, g(R, K[i]) ^ L 
    L = g(R, K[3]) ^ L
    return (L << 8) ^ R 

def main():
    k = getrandbits(32)
    time_start = time()
    print('List of actions:')
    print('0) Exit')
    print('1) Encrypt')
    print('2) Get Flag')
    while True:
        print('Select an action:')
        actions = input()
        if actions == '0':
            break
        elif actions == '1':
            print('Enter the encryption block:')
            m = int(input(), 16)
            if m >= (1 << 16):
                print('Too big for the block')
                continue
            print(f'encrypt: {hex(encrypt(m, k)) [2:]}')
        elif actions == '2':
            print('Enter the key:')
            key = int(input(), 16)
            if key == k:
                print('You guessed the key')
                if time() - time_start > 1:
                    print("But you're too late")
                else:
                    print(flag)
            else:
                print('The key is not correct')
            break
    
if __name__ == "__main__":
    main()
