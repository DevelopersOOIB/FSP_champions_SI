# Random generator
**Описание**: Я изучаю ТПСГ. Скажи я правильно шифрую данные?
У нас есть часть начального текста, а значит мы можем получить начало ключа. То есть часть случайной последовательности. Её уже можно проанализировать и понять с каким генератором мы имеем дело. 
Получаем последовательность: $25, 254, 119, 212, 165, 186, 35, 48, 113, 182, 15, 204$
Так как последовательность небольшая, то придётся использовать только графические методы анализа. Самый стандартный это рассмотреть распределение точек на плоскости.
![alt text](image-3.png)
Точек немного, однако достаточно, чтобы заметить линейную зависимость. А значит это линейный конгруэнтный генератор. Осталось найти его коэффициенты, так как модуль уже известен – это 256.
Для нахождения флага можно реализовать следующий код на языке **Python**:
```python
import matplotlib.pyplot as plt

def distribution_of_points(A):
    plt.scatter(A[:-1], A[1:], 5)
    plt.xlabel('Элемент последовательности')
    plt.ylabel('Следующий элемент')
    plt.title('Распределение точек')
    plt.show()

def getkey(A):
    global m, a, b
    m = 256
    a = ((A[1] - A[2]) * pow(A[0] - A[1], -1, m)) % m
    b = (A[1] - A[0]*a) % m

def next(seed):
    return (seed*a + b) % m

def decrypt(ctext, seed):
    text = [0] * len(ctext)
    for i in range(len(ctext)):
        text[i] = ctext[i] ^ seed
        seed = next(seed)
    return bytes(text)

def main():
    with open('output.txt', 'rb') as file:
        ctext = file.read()
    text = b'flag{random_'
    A = [text[i] ^ ctext[i] for i in range(len(text))]
    print(A)
    distribution_of_points(A)
    getkey(A)
    print(decrypt(ctext, A[0]))

if __name__ == "__main__":
    main()
```
**Ответ**: flag{random_g3N3rAt0r_mUst_b3_sTaB13}
