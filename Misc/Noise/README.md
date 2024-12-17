# Writeup

таск на стегу флаг спрятан в шуме, код решения 

``` Python
from PIL import Image


image_path = "underwater_noise.png"
image = Image.open(image_path)
pixels = image.load()
width, height = image.size
extracted_bits = []
for y in range(height):
    for x in range(width):
        blue_channel = pixels[x, y][2]
        extracted_bits.append(str(blue_channel & 1))  # LSB

binary_data = ''.join(extracted_bits)

bytes_data = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]

flag = ''.join([chr(int(byte, 2)) for byte in bytes_data if int(byte, 2) != 0])

print("Извлечённый флаг:", flag)
```

# Flag

flag{st3g_n0is3_in_fl4g}
