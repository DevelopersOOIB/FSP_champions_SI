# Описание: 
форензики принесли какой-то странный файл, не знают что с ним делать, возьмешься ?

# Решение 
С помощью утилиты olevba сдампить исходный код vba макроса, далее понять какие переменные есть, раскодировать строку из ip port
```vba
Const lsjhskjdfh = Chr(49) & Chr(48) & Chr(46) & Chr(50) & Chr(50) & Chr(46) & Chr(55) & Chr(56) & Chr(46) & Chr(50) & Chr(50)

Const sdfhsljh = "Chr(49) & Chr(51) & Chr(51) & Chr(55)
```
с помощью таблицы символов ASCII 49 48 46 50 50 46 55 56 46 50 50 49 51 51 55 и получить валидный ip 10.22.78.22 и порт 1337, что и будет флагом-iocом 

# Flag
flag{10.22.78.22:1337}