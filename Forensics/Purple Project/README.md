# Описание 

Анализируем pcap, видим множество запросов POST к URL /admin.php
Вытаскиваем параметры и значения POST-запросов
```
tshark -r suspicious_admin_panel.pcapng -Y "http.request.method == \"POST\" and http.request.uri contains \"/admin.php\"" -T fields -e http.file_data | grep -o 'cookie=[^&]*' > cookies.txt
```
Вытаскиваем соответствующие ответы:
```
tshark -r suspicious_admin_panel.pcapng -Y "http.response and ip.src == 192.168.11.146" -T fields -e http.file_data > responses.txt
```
Находим закономерность: в ответах и в запросах есть одинаковые начала строк, а содержимое напоминает base64, хоть напрямую и не декодируется. Навернаяка эти совпадающие паттерны строк и есть реальное их начало.
Проверяем в cyberchef, удалив первые 2 символа из значения cookie, а дальше cyberchef сам предлагает дважды раскодировать из base64. 
С ответом почти то же самое, только удаляем первые 3 символа.

Поняв, как нам действовать, пишем скрипт декодер:
```
import base64
from urllib.parse import unquote

def process_file(input_file, output_file, char_offset, separator):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line_number, line in enumerate(infile, start=1):
            processed_line = line[char_offset:].strip()

            try:
                url_decoded_line = unquote(processed_line)
                first_decode = base64.b64decode(url_decoded_line).decode('utf-8')
                second_decode = base64.b64decode(first_decode).decode('utf-8')
                outfile.write(f"{line_number}{separator}{second_decode}\n")
            except Exception as e:
                print(f"Ошибка при обработке строки {line_number}: {e}")

cookies_file = 'cookies.txt'
responses_file = 'responses.txt'
output_file = 'output.txt'
cookie_offset = 9
response_offset = 3 
separator = ' | ' 

process_file(cookies_file, 'cookies_output.txt', cookie_offset, separator)
process_file(responses_file, 'responses_output.txt', response_offset, separator)

print("Обработка завершена. Результаты записаны в 'cookies_output.txt' и 'responses_output.txt'.")
```
Далее изучаем запросы:
```
cat cookies_output.txt
```
Находим следующую строку:
```
30 | echo getcwd()."$ "; system('getent passwd');
31 | echo getcwd()."$ "; system('cat ../flag.txt | base64');
32 | echo getcwd()."$ "; system('lsof | wc -l');
```
Ищем соответствующий ответ:
```
cat responses_output.txt | egrep '^31'
31 | /var/www/html$ ZmxhZ3tuM3R3MHJrXzRuNl9tNHlfYjNfMW50M3IzNXQxbmdfNG5kX24wdF81MF8zNDV5fQo=
```
Декодируем:
```
echo 'ZmxhZ3tuM3R3MHJrXzRuNl9tNHlfYjNfMW50M3IzNXQxbmdfNG5kX24wdF81MF8zNDV5fQo=' | base64 -d
```
flag{n3tw0rk_4n6_m4y_b3_1nt3r35t1ng_4nd_n0t_50_345y}
