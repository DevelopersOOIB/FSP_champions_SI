# Описание
Автор @geen_stack

Это классика, это знать надо

Ссылка на материалы

https://drive.google.com/file/d/1gBAZABCgSAYB7TDdqgSi9MsZhcXi8Bxw/view?usp=drive_link

# WriteUp

Это дамп трафика, в котором есть ICMP-эксфильтрация. Чтобы чутка запутать игроков, я делал перерывы между отправкой пакетов и в целом весь процесс передачи данных шумел.
Восстановить данные можно скриптом:
```
from scapy.all import rdpcap, ICMP

def extract_flag(pcap_file, output_file):
    try:
        packets = rdpcap(pcap_file)
        extracted_data = b""

        for packet in packets:
            if packet.haslayer(ICMP) and packet[ICMP].type == 8:  # Эхо-запрос
                data = bytes(packet[ICMP].payload)
                if data == b"EOF":
                    print("Достигнут конец данных. Сохраняем флаг.")
                    break
                extracted_data += data

        # Сохранение извлеченных данных в файл
        with open(output_file, 'wb') as f:
            f.write(extracted_data)

        print(f"Флаг успешно восстановлен и сохранен в {output_file}.")

    except Exception as e:
        print(f"Ошибка при обработке PCAP: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Использование: python extract_flag.py <pcap_file> <output_file>")
        sys.exit(1)

    pcap_file = sys.argv[1]
    output_file = sys.argv[2]
    extract_flag(pcap_file, output_file)

```

## Flag
```
flag{1cmp_3xf1ltr4t10n_1s_cl4ss1c}
```
