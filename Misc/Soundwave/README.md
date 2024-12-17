# Описание задания:

Говорят, музыка — это язык, понятный всем. А что, если в этой мелодии скрыто нечто большее? 

LSB стеганография в амплитудных значениях аудиосемплов.

# Решение:

```
import wave
import numpy as np


audio_path = "music.wav"
with wave.open(audio_path, "r") as wav_file:
    params = wav_file.getparams()
    frames = wav_file.readframes(params.nframes)
    audio_data = np.frombuffer(frames, dtype=np.int16)

extracted_bits = []
for sample in audio_data:
    extracted_bits.append(sample & 1)

binary_data = ''.join(map(str, extracted_bits))
bytes_data = [binary_data[i:i + 8] for i in range(0, len(binary_data), 8)]
message = ''
for byte in bytes_data:
    try:
        char = chr(int(byte, 2))
        message += char
    except ValueError:
        break

print("Результат извлечения:", message[:50])
```

# Flag: 

flag{hidden_in_audio_wave}
