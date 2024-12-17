# Описание**: 

Нам нужен флаг

# Writeup

Перед нами шифр **RSA** и фактически происходит отправка двух похожих сообщений, которые отличаются друг от друга только добавлением подписи. А значит эти сообщения уязвлены к атаке Франклина-Рейтера. Так как сообщения связаны линейной функцией $m_2=2^{256} m_1+s$. Осталось только подобрать s, но это не трудно, так как судя по выбору порождающего члена он имеет малый порядок, а значит цифровых подписей может быть немного. Значит перебираем пока не получится сообщение.
Код на языке **Python**:
```python
from Polynom import Poly, gcd
from hashlib import sha256
from Cryptodome.Util.number import long_to_bytes, bytes_to_long

n = 38577…601
e = 199
g = 25281…476
c1 = 23445…683
c2 = 72287…205

def sign(g, n, s):
    return sha256(long_to_bytes(pow(g, s, n))).digest()

def getM(a, b):
    P1 = Poly([0, 1], n)**e - Poly([c1], n)
    P2 = Poly([b, a], n)**e - Poly([c2], n)
    M = gcd(P1, P2)
    if M.coef == [1]:
        return None
    else:
        return (-M.coef[0]) % n

def main():
    a = 1 << 256
    r = g
    b_list = [bytes_to_long(sha256(long_to_bytes(r)).digest())]
    while r != 1:
        r = (r * g) % n
        b_list.append(bytes_to_long(sha256(long_to_bytes(r)).digest()))
    for b in b_list:
        m = getM(a, b)
        if m != None:
            flag = long_to_bytes(m)
            break
    print(flag)

if __name__ == "__main__":
    main()
```
**Ответ**: flag{RSA_1s_vuln3rabl3_l3arn_t0_us3_1t} 
