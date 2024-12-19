import psycopg2
from psycopg2.extras import NamedTupleCursor
import os
import uuid
import hashlib
import json


DATABASE_URL = os.getenv("DATABASE_URL")


def generate_account_number():
    random_uuid = str(uuid.uuid4()).replace("-", "")
    account_number = ""
    for i in random_uuid:
        account_number += str(ord(i))

    return account_number


def connect_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('DROP TABLE IF EXISTS buckets')
    cursor.execute('DROP TABLE IF EXISTS orders')
    cursor.execute('DROP TABLE IF EXISTS products')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            login TEXT NOT NULL,
            password TEXT NOT NULL,
            account_number TEXT NOT NULL,
            avatar TEXT NOT NULL DEFAULT 'no-avatar.png',
            balance INTEGER DEFAULT 1000
        )               
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            photo TEXT NOT NULL,
            price INTEGER,
            flag TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buckets (
            id TEXT PRIMARY KEY,
            user_id INTEGER,
            product_id INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            user_id INTEGER,
            product_id INTEGER
        )
    ''')


    cursor.execute("ALTER SEQUENCE users_id_seq RESTART WITH 1000")



    with open('names.txt', 'r') as f:
        names = f.readlines()

    for name in names:
        name = name.strip()
        balance = 1000
        account_number = generate_account_number()
        if name == 'Magnat':
            balance = '999999'

        password = str(uuid.uuid4())
        password = hashlib.md5(password.encode())
        password = password.hexdigest()

    
        cursor.execute('''
            INSERT INTO users (login, password, account_number, balance)
            VALUES (%s, %s, %s, %s)
        ''', 
        (name, password, account_number, balance)
        )
    
    with open('products.json', 'r') as f:
        products = json.loads(f.read())

    for product in products:
        cursor.execute('''
            INSERT INTO products (name, description, photo, price, flag) VALUES
            (%s, %s, %s, %s, %s)
        ''',
        (product['name'], product['description'], product['photo'], product['price'], product['flag'],)
        )

    conn.commit()
    conn.close()


def login(login, password):

    try:
        conn = connect_db()
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)
        #cursor = conn.cursor()
        password = hashlib.md5(password.encode())
        password = password.hexdigest()
        
        cursor.execute('SELECT id FROM users WHERE login = %s AND password = %s', (login, password,))

        user = cursor.fetchone()
        #columns = [desc[0] for desc in cursor.description]
        #user = [dict(zip(columns, row)) for row in rows]

        conn.close()

        if not user:
            return False

        return {"id":user.id} 
    except Exception as e:
        return False


def check_if_login_taken(login):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE login = %s", (login,))
        user = cursor.fetchone()
        conn.close()

        if user:
            return True
        
        return False
    
    except Exception as e:
        return True
    

def create_account(login, password):
    try:
        conn = connect_db()
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)

        password = hashlib.md5(password.encode())
        password = password.hexdigest()

        account_number = generate_account_number()
        cursor.execute('''
            INSERT INTO users (login, password, account_number)
            VALUES (%s, %s, %s)
        ''', 
        (login, password, account_number,)
        )

        cursor.execute('SELECT * FROM users WHERE login = %s', (login, ))
        user = cursor.fetchone()

        conn.commit()
        conn.close()

        if user:
            return {"id":user.id}
        
        return False

    except Exception as e:
        return False

def proflie(user_id):
    try:
        conn = connect_db()
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)

        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            return False
        
        user = {
            "id":user.id,
            "login":user.login,
            "avatar":user.avatar,
            "account_number":user.account_number,
            "balance":user.balance
        }

        return user
    except Exception as e:
        return False

def shop():
    try:
        conn = connect_db()
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)

        cursor.execute('SELECT id, name, description, photo, price FROM products')
        products = cursor.fetchall()

        conn.close()

        if not products:
            return False
        
        result = []

        for product in products:
            result.append({
                "id":product.id,
                "name":product.name,
                "description":product.description,
                "photo":product.photo,
                "price":product.price
            })

        return result
    except Exception as e:
        return False


def get_account_number(user_id):
    try:
        conn = connect_db()
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)

        cursor.execute('SELECT account_number FROM users WHERE id = %s', (user_id,))

        account_number = cursor.fetchone()
        conn.close()

        if not account_number:
            return False
        
        return account_number.account_number

    except Exception as e:
        return False

def add_product_to_bucket(user_id, product_id):
    #return False
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products WHERE id = %s", (int(product_id), ))
        product = cursor.fetchone()

        if not product:
            conn.close()
            return False
        
        bucket_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO buckets (id, user_id, product_id) VALUES (%s, %s, %s)"
            , (bucket_id, user_id, product_id,)
        )

        cursor.execute("SELECT * FROM buckets WHERE id = %s", (bucket_id,))
        bucket = cursor.fetchone()
        conn.commit()
        conn.close()

        if not bucket:
            return False
        
        return True

    except Exception as e:
        return False


def delete_from_bucket(bucket_id, user_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM buckets WHERE id = %s AND user_id = %s", (bucket_id, user_id,))
        conn.commit()

        conn.close()
        return True
    except Exception as e:
        return False


def clear_bucket(user_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM buckets WHERE user_id = %s", (user_id,))
        conn.commit()

        conn.close()
        return True
    except Exception as e:
        return False


def bucket(user_id):
    try:
        conn = connect_db()
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)

        cursor.execute("SELECT * FROM buckets WHERE user_id = %s", (user_id, ))
        buckets = cursor.fetchall()
        
        if not buckets:
            conn.close()
            return False

        result = []

        for bucket in buckets:
            bucket_id = bucket.id

            cursor.execute("SELECT name, description, photo, price FROM products WHERE id = %s", (bucket.product_id,))
            product = cursor.fetchone()

            product_name = product.name
            product_description = product.description
            product_photo = product.photo
            product_price = product.price

            result.append({
                "id":bucket_id,
                "name":product_name,
                "description":product_description,
                "photo":product_photo,
                "price":product_price
            })

        conn.close()

        return result
    except Exception as e:
        return False


def pay(bucket_id, account_number, user_id):
    try:
        conn = connect_db()
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)
        
        #Проверяем что есть такой номер счета (сразу выбираем баланс)
        cursor.execute("SELECT id, balance FROM users WHERE account_number = %s", (account_number,))
        user_id_and_balance = cursor.fetchone()

        if not user_id_and_balance:
            conn.close()
            return False
        
    
        balance = user_id_and_balance.balance
        #user_id = user_id_and_balance.id

        #Проверяем что есть такая корзина (сразу выбираем ID-продукта из корзины)
        cursor.execute("SELECT product_id FROM buckets WHERE id = %s", (bucket_id,))
        product_id = cursor.fetchone()

        if not product_id:
            conn.close()
            return False
        
        product_id = product_id.product_id

        #Выбираем продукт по ID
        cursor.execute("SELECT price FROM products WHERE id = %s", (product_id, ))
        product = cursor.fetchone()

        if not product:
            conn.close()
            return False
        
        #Чекаем что баланс норм, если не норм - сообщение о том что не хватает денег
        if balance < product.price:
            conn.close()
            return {"error":"Недостаточно средств"}
        
        #Вычитаем из баланса юзера цену товара
        balance = balance - product.price
        cursor.execute("UPDATE users set balance = %s WHERE account_number = %s", (balance, account_number))

        #Удаляем корзину
        cursor.execute('DELETE FROM buckets WHERE id = %s', (bucket_id,))
        
        #Создаем заказ
        order_id = str(uuid.uuid4())
        cursor.execute(
            "INSERT INTO orders (id, user_id, product_id) VALUES (%s, %s, %s)",
            (order_id, user_id, product_id,)
        )

        if product_id == 5:
            cursor.execute("UPDATE users SET balance = 999999 WHERE login = 'Magnat'")

        conn.commit()
        conn.close()
        return {"order_id":order_id}

    except Exception as e:
        return False


def pay_all(user_id):
    try:
        conn = connect_db()
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)

        #Выбрать баланс по айди юзера
        cursor.execute("SELECT balance FROM users WHERE id = %s", (user_id,))
        balance = cursor.fetchone()

        if not balance:
            conn.close()
            return False
        
        balance = balance.balance

        #Выбрать все элементы в корзине
        cursor.execute("SELECT product_id FROM buckets WHERE user_id = %s", (user_id,))
        buckets_products = cursor.fetchall()

        if not buckets_products:
            conn.close()
            return {"error":"Корзина пуста"}

        #Пройтись циклом по элементам корзины, дернуть товары по айдишникам, дернуть из них прайсы и сложить в большой прайс 
        bucket_price = 0
        for bucket_product in buckets_products:
            product_id = bucket_product.product_id
            cursor.execute("SELECT price FROM products WHERE id = %s", (product_id,))
            price = cursor.fetchone()
            bucket_price += price.price

        #Сравнить балансы
        if balance < bucket_price:
            conn.close()
            return {"error":"Недостаточно средств"}

        #Вычесть баланс юзера и обновить
        balance = balance - bucket_price
        cursor.execute("UPDATE users SET balance = %s WHERE id = %s", (balance, user_id))
    
        #Пройтись в цикле по элементам корзины и добавлять новый заказ юзеру
        for bucket_product in buckets_products:
            product_id = bucket_product.product_id

            ### Вот здесь еще всатвить код чтобы вернуть денег магнату
            if product_id == 5:
                cursor.execute("UPDATE users SET balance = 999999 WHERE login = 'Magnat'")

            order_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO orders (id, user_id, product_id) VALUES (%s, %s, %s)",
                (order_id, user_id, product_id,)
            )
    
        #Очистить корзину юзера
        cursor.execute("DELETE FROM buckets WHERE user_id = %s", (user_id,))
        conn.commit()
        conn.close()

        return {"success":"OK"}
    except Exception as e:
        return False

def orders(user_id):
    try:
        conn = connect_db()
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)

        cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id,))
        orders = cursor.fetchall()

        if not orders:
            conn.close()
            return False
        
        orders_result = []

        for order in orders:
            order_id = order.id
            product_id = order.product_id

            cursor.execute("SELECT name, photo FROM products WHERE id = %s", (product_id,))
            procut = cursor.fetchone()

            orders_result.append({
                "id":order_id,
                "name":procut.name,
                "photo":procut.photo
            })

        conn.close()
        return orders_result

    except Exception as e:
        return False


def order_by_id(user_id, order_id):
    #name, photo, description, flag
    try:
        conn = connect_db()
        cursor = conn.cursor(cursor_factory=NamedTupleCursor)

        cursor.execute("SELECT product_id FROM orders WHERE id = %s", (order_id,))
        order = cursor.fetchone()

        if not order:
            conn.close()
            return False
        
        cursor.execute("SELECT name, description, photo, flag FROM products WHERE id = %s", (order.product_id,))
        product = cursor.fetchone()

        flag = product.flag
        if flag == 'no':
            flag = 0

        conn.close()

        return {"name":product.name, "description":product.description, "photo":product.photo, "flag":flag}
    except Exception as e:
        return False


def check_access_to_order(user_id, order_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE user_id = %s AND id = %s", (user_id, order_id,))
        order = cursor.fetchone()
        conn.close()

        if not order:
            return False
        
        return True
    
    except Exception as e:
        return False