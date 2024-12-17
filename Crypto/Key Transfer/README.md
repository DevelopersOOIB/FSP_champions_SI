# Описание:

Я придумал сервис для хранения закрытых людей в открытом канале. Можешь сам проверить.

# Writeup

Перед нами сервер, который выдает вда открытых ключа RSA. И отправляет два сообщения содержащих линейные комбинации простых чисел, на которы раскладывается n: 

<img width="343" alt="image" src="https://github.com/user-attachments/assets/71a1f5d1-3622-4d3b-a207-1c4ca700746c" />

Для того, чтобы получить числа p и q необходимо выразить такое число, чтобы оно делилось на p. А после искать через НОД. Для этого воспользуемся следующим свойством:

<img width="474" alt="image" src="https://github.com/user-attachments/assets/1e737a58-22db-4b53-9b7b-4e4fe97b26b0" />

Так как все другие слагаемые будут содержать pq = n. Тогда можно выразить число делящиеся на p следующим образом:

<img width="627" alt="image" src="https://github.com/user-attachments/assets/718314dc-911c-4144-b892-e58b81d93589" />

То есть $\frac{c_1^{e_2}}{7^{e_1 e_2}} - \frac{c_2^{e_1}}{3^{e_1 e_2}}$  – делится на p. А значит возводя его в любую степень будем также получать тоже число, которое делится на p и таким образом найдём число p с помощью **НОД**. 

Для решения можно составить следующий код на языке **Python**:
```python
import telnetlib

HOST = "192.168.153.128"
PORT = 4441

tn = telnetlib.Telnet(HOST, PORT)

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def main():
    n = int(tn.read_until(b"\n")[4:])
    e1 = int(tn.read_until(b"\n")[5:])
    e2 = int(tn.read_until(b"\n")[5:])
    c1 = int(tn.read_until(b"\n")[5:])
    c2 = int(tn.read_until(b"\n")[5:])
    c1 = pow(c1, e2, n)
    c2 = pow(c2, e1, n)
    c1 = c1 * pow(7, -e1*e2, n)
    c2 = c2 * pow(3, -e1*e2, n)
    r = (c1 - c2) % n
    p = r
    while n % p:
        r = (r * (c1 - c2)) % n
        p = gcd(p, r)
    q = n // p
    tn.read_until(b"\n")
    tn.write(f'{p}'.encode() + b'\n')
    tn.read_until(b"\n")
    tn.write(f'{q}'.encode() + b'\n')
    print(tn.read_until(b"\n"))

if __name__ == "__main__":
    main()
```
**Ответ**: flag{key_transfer_is_strictly_according_to_protocols} 
