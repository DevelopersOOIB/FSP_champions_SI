# Опсиание
Автор @geen_stack

Еще один вариант классической эксфильтрации


# WriteUp

Это дамп трафика, в котором есть HTTP-эксфильтрация. Чтобы чутка запутать игроков, я делал перерывы между отправкой пакетов и в целом весь процесс передачи данных шумел. Кроме того, сами данные кодируются hex, после чего строка переворачивается
Восстановить данные можно скриптом:
```
from scapy.all import rdpcap, TCP
from urllib.parse import unquote

def extract_file_from_pcap(pcap_file, output_file):
    try:
        packets = rdpcap(pcap_file)
        data_chunks = []

        for packet in packets:
            # Фильтруем HTTP GET-запросы
            if packet.haslayer(TCP) and packet[TCP].dport == 80:  # Порт 80 (HTTP)
                payload = bytes(packet[TCP].payload).decode(errors="ignore")

                # Ищем строки GET с параметром data
                if "GET /?" in payload and "data=" in payload:
                    start = payload.find("data=") + len("data=")
                    end = payload.find(" ", start)
                    if end == -1:
                        continue
                    encoded_data = payload[start:end]
                    
                    # Декодируем из URL (unquote)
                    chunk = unquote(encoded_data)
                    
                    # Добавляем в список данных
                    if chunk == "EOF":
                        print("Маркер завершения найден. Заканчиваем восстановление.")
                        break
                    data_chunks.append(chunk)

        # Восстанавливаем файл из данных
        with open(output_file, 'wb') as f:
            for chunk in data_chunks:
                decoded_chunk = bytes.fromhex(chunk[::-1])  # Переворачиваем строку и декодируем hex
                f.write(decoded_chunk)

        print(f"Файл успешно восстановлен и сохранен в {output_file}.")

    except Exception as e:
        print(f"Ошибка при обработке PCAP: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Использование: python recover_file_from_pcap.py <pcap_file> <output_file>")
        sys.exit(1)

    pcap_file = sys.argv[1]
    output_file = sys.argv[2]
    extract_file_from_pcap(pcap_file, output_file)

```

## Flag
```
flag{w3bh00k_3xf1ltr4t10n}
```
