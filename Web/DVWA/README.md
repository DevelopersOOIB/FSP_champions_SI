# Writeup 

попадаем на такую страничку

<img width="940" alt="image" src="https://github.com/user-attachments/assets/f052ad10-2611-412c-b14e-372c283a533f" />

есть форма регистрации, куки, фальшивая бд с проверкой на инъекцию, всё чтобы отвлечь участников, на страницк /admin мы ловим 403 ошибку

<img width="1005" alt="image" src="https://github.com/user-attachments/assets/f80a5c70-0ab5-4171-b16e-e5535f3d17e4" />

чтобы получить флаг, нужно сменить метод на HEAD, флаг будет в заголовках

<img width="1005" alt="image" src="https://github.com/user-attachments/assets/adaea91a-bee8-40e9-ab33-c8e2a64027f8" />

# Flag 

flag{byp4ss_http_m3thod}
