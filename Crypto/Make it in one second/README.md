# Описание: 
Я разработал легковесный шифр. Я знаю, что он слабый, но актуальность ключа теряется спустя 1 секунду после генерации ключа, так что надёжным он быть не должен. Проверь мой шифр.

# Writeup
Перед нами сервер, который через 1 секунду после запуска перестаёт давать флаг и за это время необходимо получить ключ. 
Оценим шифр. Это очень урезанная магма на 4 раунда с длиной блока 2 байта и ключом 4 байта. То есть для того, чтобы подобрать ключ необходимо $2^{32}$ переборов, но так мы точно не успеем, а значит нам необходимо использовать другой алгоритм. Можно поступить методом человек по середине. Тогда необходимо сделать только 2^16 переборов. При этом шифрую первую половину необходимо сразу упорядочивать значения по возрастанию или поиск станет трудоёмким. 
В итоге запросив одну пару открытый-закрытый текст мы получим $2^{16}$ возможных ключей. Получая последующие пары, мы сможем их отсеять простым перебором. Таким образом через 2-3 просеивания у нас останется один ключ.
Примечание: так же важно, как запускать код. К примеру, код Python гораздо быстрее запускать напрямую через интерпретатор, чем через IDE.
Код программы на языке **Python**:
```python
import telnetlib
from time import time

HOST = "192.168.153.128"
PORT = 4445

tn = telnetlib.Telnet(HOST, PORT)

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

def encrypt_2(m, k):
    k1, k2 = k & 0xff, k >> 8
    L, R = m >> 8, m & 0xff
    L, R = R, g(R, k1) ^ L 
    L, R = R, g(R, k2) ^ L 
    return (L << 8) ^ R

def decrypt_2(c, k):
    k1, k2 = k >> 8, k & 0xff
    L, R = c >> 8, c & 0xff
    L, R = R, g(R, k1) ^ L
    L = g(R, k2) ^ L 
    return (L << 8) ^ R

def get_key_list(m, c):
    n = 1 << 16
    key_list_R = [0] * n
    for key_R in range(n):
        s = encrypt_2(m, key_R)
        key_list_R[s] = key_R
    key_list = [0] * n
    for key_L in range(n):
        s = decrypt_2(c, key_L)
        key_list[s] = (key_L << 16) ^ key_list_R[s]
    return key_list

def main():
    time_start = time()
    for _ in range(4):
        tn.read_until(b'\n')
    m = 0
    tn.read_until(b'\n')
    tn.write(b'1\n')
    tn.read_until(b'\n')
    tn.write(f'{hex(m)}'.encode() + b'\n')
    c = int(tn.read_until(b'\n')[9:], 16)
    key_list = get_key_list(m, c)
    while len(key_list) != 1:
        m += 1
        tn.read_until(b'\n')
        tn.write(b'1\n')
        tn.read_until(b'\n')
        tn.write(f'{hex(m)}'.encode() + b'\n')
        c = int(tn.read_until(b'\n')[9:], 16)
        key_list = [k for k in key_list if encrypt(m, k) == c]
    tn.read_until(b'\n')
    tn.write(b'2\n')
    tn.read_until(b'\n')
    tn.write(f'{hex(key_list[0])}'.encode() + b'\n')
    tn.read_until(b'\n')
    print(tn.read_until(b'\n'))
    print(time() - time_start)
    input()

if __name__ == "__main__":
    main()
```
**Ответ**: flag{optimize_the_code_and_you_will_be_happy}
