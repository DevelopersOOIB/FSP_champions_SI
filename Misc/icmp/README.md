# Опиcание
Автор @geen_stack
Мы заметили странную сеетвую активность. Кто-то искал в сети живые хосты чтобы совершать на них атаки?

# WriteUp

Если изучить дамп трафика, то можно заметить, что пинуются хосты из сети 192.168.1.0/24, отличаются только последние октеты.
Если посмотреть на эти октеты еще внимательнее и перевести их в символы как ASCII - то мы получим флаг

# Flag
```
flag{1_h1d3_m3ss4g4_1n_1pv4_0ct3ts}
```
