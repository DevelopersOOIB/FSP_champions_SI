# Writeup

В иде сразу видим два массива хексов 
<img width="1797" alt="image" src="https://github.com/user-attachments/assets/bf005040-6d9f-4e2e-a6a1-a24a5e99758d" />

После ввода флага вызывается 3 функции:

<img width="919" alt="image" src="https://github.com/user-attachments/assets/d3c7f649-7fe6-4189-b2b7-f243df57c24c" />

Математика описана в каждой из них:

<img width="1111" alt="image" src="https://github.com/user-attachments/assets/50674137-f1a5-4dbc-ba4a-3f5ae4e789d8" />

<img width="932" alt="image" src="https://github.com/user-attachments/assets/27b402b2-b1d4-487d-afb8-c595b445bdc9" />

Применяем ее к хексам, получаем пару ключей шифрования:
```
key1 = 'k3y_for_3cryp71ion_k3y
key2 = 'w0w_encryp7ion_key'
```
Далее смотрим в encrypt() и пишем обратный код:

<img width="918" alt="image" src="https://github.com/user-attachments/assets/b0965fed-c020-419d-9f6f-5426b9353f35" />

Солвер целиком:
```
v20 = 'ac8396888389993d5a934598a771f6829aaf'
v21 = 'd49cdef8a3e8dff89cacdfdee99096aee8ebf8d49cde'

def decr0(a):
    r = b''
    for i in a:
        t = i ^ 0x36
        t = (t - 125) % 256
        t = t ^ 0x25
        t = (t - 118) % 256
        t = t ^ 0x96 ^ 0x37
        r += bytes.fromhex(hex(t)[2:].zfill(2))
    return r

def decr1(a, b):
    r = b''
    for i in range(len(a)):
        t = (a[i] - 88) % 256
        t = t ^ 0x7f
        t = (t + 26) % 256
        t = t ^ 0x33
        t = (t - 90) % 256
        t = t ^ b[i%len(b)]
        r += bytes.fromhex(hex(t)[2:].zfill(2))
    return r

k1 = b'k3y_for_3cryp71ion_k3y'
k2 = b'w0w_encryp7ion_key'
def decr(a, b):
    b2 = b''
    for i in range(len(a)):
        t = (a[i] + 68) % 256
        t = t ^ 0x43
        t = (t - 50) % 256
        t = t ^ 0x56 ^ 0xEF ^ b[i%len(b)]
        b2 += bytes.fromhex(hex(t)[2:].zfill(2))
    return b2
ct = bytes.fromhex('55105eac565f1b4f4e4c6b1762b5ac1363223c6f574119655e595547280d6a63646e15615721')

t = decr0(bytes.fromhex(v21))
print(t)
t = decr1(bytes.fromhex(v20), t)
print(t)
print(decr(ct, t))
```
