# Backpack
Описание: 

Старый добрый шифр рюкзака. Примечание: во флаге не содержится цифр

# Writeup

Это действительно обычный шифр рюкзака и у нас полностью реализованная шифр система. Шифр рюкзака действительно сейчас считается почти не применимым на практике, так как существует LLL алгоритм, который позволяет найти какие элементы нужно взять, чтобы получить элемент. Но данный рюкзак хороший, он достаточно плотный, а значит LLL в качестве наименьших векторов будет выражать элементы рюкзака друг через друга. Значит необходимо оптимизировать и как-то помочь LLL алгоритму.
Нам не просто так дана подсказка, что в флаге не содержится цифр. Так как остальные символы в флаге – это большие, маленькие и символы “_”, “}”. У всех у них есть особенность. В их байтовом представлении старшие биты равны 01. А значит мы точно знаем, что каждый восьмой элемент рюкзака, начиная с первого, брался, значит их можно убрать из LLL алгоритма. Так же каждый восьмой элемент рюкзака, начиная со второго, брался, значит от всех зашифрованных сообщений можно вычесть их сумму и тоже убрать их LLL алгоритма. Теперь у нас не 64 элемента рюкзака, а 48 бит. Но он всё ещё плотный и буквально не хватает убрать ещё пару элементов. Для этого мы используем метод встречи по середине комбинированный с LLL алгоритмом. То есть мы будем подбирать один символ шифртекста, считать какую сумму он должен был дать, потом отнимать её от шифртекста и тем самым убирать ещё 6 бит. Для 42 элементов данный рюкзак не устойчив к LLL алгоритму. Таким образом можно расшифровать каждый зашифрованный блок.
Примечание: Полный перебор потребуется только для среднего блока, так как в нём вообще никакого символа не известно. Первый блок в конце должен содержать “}”. Последний блок в начале “flag{”
Для нахождения флага используем следующий код:
```python
from Cryptolib import LLL
from Cryptodome.Util.number import bytes_to_long

Alf = [a for a in range(ord('a'), ord('z') + 1)] + \
      [ord('}'), ord('_')] + \
      [a for a in range(ord('A'), ord('Z') + 1)]

B = [22013…589, 20441…493, 29335…833, …, 29945…874, 28155…244]
C = [611875063875452181270177525150, 610830665829814487671341795820, 640746993403996414294125775482]

def decrypt_LLL(c, B):
    N = 1 << 128
    Matrix = [[1 if i == j else 0 for j in range(len(B))] + [N*B[i]] for i in range(len(B))] + \
             [[0 for i in range(len(B))] + [N*c]]
    Matrix = LLL(Matrix)
    for b in Matrix:
        if all([i == 1 or i == 0 or i == -1 for i in b[:-1]] + [b[-1] == 0]):
            s = sum([B[i]*abs(b[i]) for i in range(len(B))])
            if s == c:
                return [abs(i) for i in b[:-1]]
    return None

def sum_B(n):
    return sum([B[i] if n & (1 << (len(B) - i - 1)) else 0 for i in range(len(B))])

def decrypt_block(c):
    for a in Alf:
        print(chr(a))
        Left = decrypt_LLL(c - sum_B(a & 0b111111), B[:42])
        if Left != None:
            Res = Left + [(a >> (5 - i)) & 1 for i in range(6)]
            Res = [int('01' + ''.join([str(j) for j in Res[i*6: i*6 + 6]]), 2) for i in range(8)]
            return bytes(Res)
        
def decrypt_block0(c):
    a = ord('}')
    Left = decrypt_LLL(c - sum_B(a & 0b111111), B[:42])
    if Left != None:
        Res = Left + [(a >> (5 - i)) & 1 for i in range(6)]
        Res = [int('01' + ''.join([str(j) for j in Res[i*6: i*6 + 6]]), 2) for i in range(8)]
        return bytes(Res)
    
def decrypt_block_last(c):
    int_f = 0
    for i in b'flag{\x00\x00\x00':
        int_f <<= 6
        int_f ^= i & 0b111111
    Rait = decrypt_LLL(c - sum_B(int_f), B[-18:])
    if Rait != None:
        Res = [int('01' + ''.join([str(j) for j in Rait[i*6: i*6 + 6]]), 2) for i in range(3)]
        return b'flag{' + bytes(Res)

def decrypt(C):
    global B
    sum_c = sum([b for b in B[1::8]])
    B = [b for i in range(8) for b in B[i*8 + 2: i*8 + 8]]
    Res = decrypt_block0(C[0] - sum_c)
    print(Res)
    for i in range(1, len(C) - 1):
        Res = decrypt_block(C[i] - sum_c) + Res
        print(Res)
    Res = decrypt_block_last(C[2] - sum_c) + Res
    return Res
                
def main():
    print(decrypt(C))
    
if __name__ == "__main__":
    main()
```
**Ответ**: flag{It_oO_thEre_is_LLL}
