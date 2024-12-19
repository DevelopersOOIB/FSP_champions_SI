# armorgedon.exe Writeup

## Первый способ решения

### Шаги:
1. **Анализ бинарника:**
   Декомпилируем файл и видим, что он запускается через `pyarmor`:
   ```
   # Version : Python 3.11

   from pyarmor_runtime_000000 import __pyarmor__
   __pyarmor__(__name__, __file__, b'PY000000\x00\x03\x0b\x ...")
   ```
   Решаем не углубляться в реверсинг `pyarmor` и начинаем анализ его поведения.

2. **Запуск и отладка:**
   При запуске видим ошибку:
   ```
   Activation server is not responsible: HTTPSConnectionPool(host='fakehost.com', port=443): Max retries exceeded with url: /fakeurl (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x0000025C23CFE150>: Failed to establish a new connection: [WinError 10061] Подключение не установлено, т.к. конечный компьютер отверг запрос на подключение'))
   ```

3. **Анализ трафика:**
   Используем Wireshark для отслеживания запросов. Обнаруживаем, что бинарник обращается не к `fakehost.com/fakeurl`, а к `backctfgamedoor.net/activate`.

4. **Изменение DNS:**
   Прописываем эти сервисы в `/etc/hosts`.

5. **Настройка сервера:**
   Запускаем HTTP сервер и видим новую ошибку:
   ```
   Activation server is not responsible: HTTPSConnectionPool(host='fakehost.com', port=443): Max retries exceeded with url: /fakeurl (Caused by SSLError(SSLError(1, '[SSL: WRONG_VERSION_NUMBER] wrong version number (_ssl.c:1002)')))
   ```

6. **Создание SSL сертификата:**
   Генерируем сертификат, используя, например, [этот гайд](https://gist.github.com/klcantrell/518d13d59c4074dbca6310c9b7e6c520).

7. **Подмена сертификата:**
   Поскольку `pyarmor` хардкодит трастовые ключи, добавление сертификата в доверенные не помогает. Поэтому при запуске приложения приостанавливаем его выполнение и заменяем файл `%TEMP%/_MEI<some number>/certifi/cacert.pem` на наш `myCA.pem`. После разморозки приложение использует уже наш сертификат.

8. **Реализация сервера активации:**
   Пишем сервер на Flask:
   ```
   from flask import Flask, jsonify, request
   import ssl
   import logging
   from datetime import datetime, timedelta, timezone

   app = Flask(__name__)

   logging.basicConfig(level=logging.DEBUG)

   @app.route('/activate', methods=['POST'])
   def activate():
       print_request_details()
       hwid = request.json.get('hwid')
       nonce = request.json.get('nonce')
       response_data = {}
       log_response(response_data)
       return jsonify(response_data)

   def print_request_details():
       app.logger.debug("Request Method: %s", request.method)
       app.logger.debug("Request URL: %s", request.url)
       app.logger.debug("Request Headers: %s", request.headers)
       app.logger.debug("Request Body: %s", request.get_data(as_text=True))
       app.logger.debug("Request JSON Data: %s", request.json)

   def log_response(response):
       app.logger.debug("Response JSON: %s", response)

   if __name__ == '__main__':
       context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
       context.load_cert_chain(certfile='kals.dev.crt', keyfile='kals.dev.key')
       app.run(ssl_context=context, host='0.0.0.0', port=443, debug=True)
   ```

9. **Исправление ошибок:**
   - После запуска бинарник выдает ошибку: `Invalid response: parameter missing`.
     Добавляем в ответ параметры `hwid` и `nonce`:
     ```
     response_data = {
         'hwid': hwid,
         'nonce': nonce,
     }
     ```
   - Следующая ошибка: `Invalid response: licence timestamp not specified`.
     Добавляем параметр `timestamp` с текущей временной меткой:
     ```
     timestamp = datetime.now(timezone.utc).timestamp()
     response_data = {
         'hwid': hwid,
         'nonce': nonce,
         'timestamp': timestamp
     }
     ```
   - Ошибка: `Invalid response: licence expired`.
     Прибавляем несколько секунд к метке времени:
     ```
     one_minute_later = datetime.now(timezone.utc) + timedelta(seconds=10)
     timestamp = one_minute_later.timestamp()
     ```
   - Ошибка: `Invalid response: licence_pass not specified`.
     Добавляем параметр `licence_pass`:
     ```
     response_data = {
         'hwid': hwid,
         'nonce': nonce,
         'timestamp': timestamp,
         'licence_pass': 0
     }
     ```
   - Ошибка: `Invalid response: licence_pass mismatch`.
     После перебора значений находим корректный ключ:
     ```python
     response_data = {
         'hwid': hwid,
         'nonce': nonce,
         'timestamp': timestamp,
         'licence_pass': '5486'
     }
     ```

10. **Флаг:**
    Получаем флаг: `flag{4rm0rg3d0n_n3tw0rk_r3sp0nc3}`.

---

## Второй способ решения

1. **Инъекция в бинарник:**
   Зная, что файл написан на Python, пытаемся исследовать его функции через инъекцию.

2. **Приостановка процесса:**
   Запускаем бинарник и саспендим его потоки (например, через Process Hacker).

3. **Инъекция Python Shell:**
   Скачиваем библиотеку `PyInjector_x64_shell.dll` с [репозитория](https://github.com/Stanislav-Povolotsky/PyInjector) и инжектим её в процесс.

4. **Анализ контекста:**
   После инъекции получаем доступ к оболочке Python и исследуем глобальные переменные:
   ```
   pyshell >>> globals()
   ...
   'decryptflag': <function decryptflag at 0x0000028B3F3158A0>
   ...
   ```

5. **Использование функции:**
   Пробуем вызвать функцию `decryptflag`:
   ```
   pyshell >>> decryptflag()
   Traceback (most recent call last):
     File "<string>", line 22, in _
     File "<string>", line 1, in <module>
   TypeError: decryptflag() missing 1 required positional argument: 'key'
   ```

6. **Подбор аргумента:**
   - Функция принимает строковый аргумент `key`.
     Пробуем брутфорсить ключ:
     ```
     pyshell >>> for i in range(999999999):
     pyshell ...     if 'flag' in decryptflag(key=str(i)):
     pyshell ...             print(decryptflag(key=str(i)))
     flag{4rm0rg3d0n_n3tw0rk_r3sp0nc3}
     ```

7. **Флаг:**
   Успешно находим ключ и получаем флаг: `flag{4rm0rg3d0n_n3tw0rk_r3sp0nc3}`.

