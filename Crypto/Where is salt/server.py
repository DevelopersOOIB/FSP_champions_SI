from random import randint

flag = 'flag{??????????????????????????}'

def isPrime(p):
    if p & 1 == 0:
        return False
    for _ in range(100):
        a = randint(2, p-2)
        if pow(a, p-1, p) != 1:
            return False
    return True

def getPrime(len_p):
    p = randint( 1 << (len_p - 1), (1 << len_p) - 1) | 1
    while not isPrime(p):
        p += 2
    return p

def getSum(num, A):
    return sum(A[:num])

def main():
    p = getPrime(1024)
    A = [randint(1 << 1023, 1 << 1024) * p  for _ in range(2**20)]
    index_salt = randint(0, len(A) - 1)
    A[index_salt] += randint(1, p - 1)
    stop = 21
    print("List of actions:")
    print("0) Exit")
    print("1) Get the sum")
    print("2) Get the flag")
    while True:
        print('Select an action:')
        actions = input()
        if actions == '0':
            break
        if actions == '1':
            if stop == 0:
                print('You will be more helpful in making this request')
            else:
                print('Enter the sum number:')
                num = int(input())
                print(getSum(num, A))
                stop -= 1
        if actions == '2':
            print('Enter the salt number')
            num_salt = int(input())
            if index_salt == num_salt:
                print(flag)
            else:
                print('The salt number was not found')
            break
                
if __name__ == "__main__":
    main()
