# Описание:

Попробуй найти среди множества чисел особое, с помощью частичных сумм. Запросов, конечно, ограниченное количество.

# Writeup
Суть задания проста, у нас есть $2^{20}$ чисел, которые делятся на одно и тоже простое число и из них одно случайное, которое не делится на это число. Мы можем запрашивать суммы чисел до определённого числа. И у нас есть 21 запрос. Таким образом можно воспользоваться бинарным поиском и найти это посоленное число. 
В начале возьмём просто первое число. С большой вероятностью оно делится на p. Далее берём сумму первой половины чисел. Если эта сумма имеет **НОД** с первым числом большим чем $2^{1024}$, то эта сумма делится на p. А значит среди них нет посоленного числа, и стоит искать в верхней половине. Продолжая бинарный поиск получим точное значение номера посоленного числа.
Для решения можно реализовать следующий кодом на языке **Python**:

```python
import telnetlib

HOST = "192.168.153.128"
PORT = 4444

tn = telnetlib.Telnet(HOST, PORT)

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def main():
    for _ in range(4):
        tn.read_until(b'\n')
    A_index_list = [bin(i)[2:].zfill(20)[::-1] for i in range(2**20)]
    sum_list = [0] * 21
    N, V = 0, 2**20
    tn.read_until(b'\n')
    tn.write(b'1\n')
    tn.read_until(b'\n')
    tn.write(f'{1}'.encode() + b'\n')
    referens = int(tn.read_until(b'\n'))
    for _ in range(20):
        num = (N + V) >> 1
        tn.read_until(b'\n')
        tn.write(b'1\n')
        tn.read_until(b'\n')
        tn.write(f'{num}'.encode() + b'\n')
        sum = int(tn.read_until(b'\n'))
        if gcd(sum, referens) > (1 << 1023):
            N = num
        else:
            V = num
    tn.read_until(b'\n')
    tn.write(b'2\n')
    tn.read_until(b'\n')
    tn.write(f'{N}'.encode() + b'\n')
    print(tn.read_until(b'\n'))

if __name__ == "__main__":
    main()

```
 **Ответ**: flag{the_method_of_binary_search_in_the_world_of_salts}
