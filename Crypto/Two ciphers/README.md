# Two Ciphers
**Описание**: Я думаю, что два шифра помогут защитить мои данные. Проверь это.

# Writeup
Мы имеем большой шифртекст и код программы. В этом коде мы видим, что действительно используются два шифра. Это шифр перестановки и шифр гаммирования. Но уязвимость в том, что у этих шифров одинаковый размер ключа. А значит перестановка никак не повлияла на статистику относительно шифра гаммирования. Из чего выходит можно найти ключ гамма и убрать его, а после убрать шифр перестановки.
Шифр гаммирования можно убрать с помощью индекса Фридмана. А перестановку вернуть с помощью критерия согласия хи квадрат относительно биграмм и реальной статистики биграмм в английском тексте.
Можно реализовать следующий код на языке **Python**:

```python
from collections import Counter
from scipy.stats import chi2

Alf = [chr(a) for a in range(ord('a'), ord('z') + 1)]
Alf_P = []
Alf_bigram = [a1 + a2 for a1 in Alf for a2 in Alf]
Alf_P_bigram = []

def get_V(text):
    V_coun = Counter(text)
    V = [0] * len(Alf)
    for a in V_coun.keys():
        V[Alf.index(a)] = V_coun[a]
    return V

def get_V_bigram(text_bigram):
    V_coun = Counter(text_bigram)
    V = [0] * len(Alf_bigram)
    for a in V_coun.keys():
        V[Alf_bigram.index(a)] = V_coun[a]
    return V

def get_P():
    global Alf_P
    global Alf_P_bigram
    with open('ref.txt', 'r') as file:
        referens = ''.join([a for a in file.read().lower() if a in Alf])
    Alf_P = [v  / len(referens) for v in get_V(referens)]
    referens_bigram = [referens[i: i + 2] for i in range(len(referens) - 1)]
    Alf_P_bigram = get_V_bigram(referens_bigram)

def index_of_matches(V):
    n = sum(V)
    return sum([v * (v-1) for v in V]) / (n * (n-1))

def mutual_index_of_coincidences(V1, V2):
    n1, n2 = sum(V1), sum(V2)
    return sum([V1[i] * V2[i] for i in range(len(V1))]) / (n1 * n2)

def mutual_index_of_coincidences_real(V):
    n = sum(V)
    return sum([V[i] * Alf_P[i] for i in range(len(V))]) / n

def chi2_bigram(V):
    n1, n2 = sum(V), sum(Alf_P_bigram)
    return n1*n2*sum([(V[i] / n1 - Alf_P_bigram[i] / n2)**2 / (V[i] + Alf_P_bigram[i]) if V[i] + Alf_P_bigram[i] != 0 else 0 for i in range(len(Alf_bigram))])

def get_len_blok(text):
    for len_blok in range(1, len(Alf)):
        V_list = [get_V(text[i::len_blok]) for i in range(len_blok)]
        stop = True
        for V in V_list:
            if index_of_matches(V) < 0.055:
                stop = False
                break
        if stop:
            break
    return len_blok, V_list

def get_key2(len_blok, V_list):
    key = [0] * len_blok
    for i in range(1, len_blok):
        for k in range(len(Alf)):
            if mutual_index_of_coincidences(V_list[0], V_list[i]) > 0.055:
                key[i] = k
                break
            V_list[i] = V_list[i][1:] + [V_list[i][0]]
    V = [sum([v[i] for v in V_list]) for i in range(len(Alf))]
    for key0 in range(0, len(Alf)):
        if mutual_index_of_coincidences_real(V) > 0.055:
            key = [(k + key0) % len(Alf) for k in key]
        V = V[1:] + [V[0]]
    return key

def get_key1(len_blok, text):
    column = [text[i::len_blok] for i in range(len_blok)]
    order = {}
    start = 0
    for i in range(len_blok):
        isStart = True
        for j in range(len_blok):
            V = get_V_bigram([column[j][k] + column[i][k] for k in range(len(column[0]))])
            if chi2_bigram(V) < chi2.ppf(0.95, len(Alf_bigram) - 1):
                order[j] = i
                isStart = False
                break
        if isStart:
            start = i
    key = [start] + [0] * (len_blok - 1)
    for i in range(1, len_blok):
        key[i] = order[key[i-1]]
    return key

def decrypt_2(text, key):
    ctext = [Alf[(Alf.index(text[i]) - key[i % len(key)]) % len(Alf)] for i in range(len(text))]
    return ''.join(ctext)

def decrypt_1(text, key):
    ctext = [text[key[i]::len(key)] for i in range(len(key))]
    return ''.join([''.join([ctext[j][i] for j in range(len(key))]) for i in range(len(text) // len(key))])

def unpad(text):
    return text[:-Alf.index(text[-1])]

def main():
    get_P()
    with open('text.txt.enc', 'r') as file:
        text = file.read()
    len_blok, V_list = get_len_blok(text)
    key2 = get_key2(len_blok, V_list)
    text = decrypt_2(text, key2)
    key1 = get_key1(len_blok, text)
    text = decrypt_1(text, key1)
    text = unpad(text)
    flag = 'flag{' + text[-text[::-1].index('galf'):] + '}'
    print(flag)

if __name__ == "__main__":
    main()
```
 **Ответ**: flag{twoindependentciphersnothelp}  
