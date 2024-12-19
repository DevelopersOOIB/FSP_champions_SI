import psycopg2
import uuid
import os


DATABASE_URL = os.getenv("DATABASE_URL")

def connect_db():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS secret')
    cursor.execute('DROP TABLE IF EXISTS types')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS secret (
            id SERIAL PRIMARY KEY,
            flag TEXT NOT NULL
        )               
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS types (
            id SERIAL PRIMARY KEY,
            type TEXT NOT NULL
        )               
    ''')

    cursor.execute("INSERT INTO types (type) VALUES (%s)", ('get_hints',))

    for i in range(0,50):
        fake_flag = "flag{FAKE_FLAG_DONT_SEND_THIS_FOR_PLATFORM_" + str(uuid.uuid4()) + "}"
        cursor.execute("INSERT INTO secret (flag) VALUES (%s)", (fake_flag, ))

    conn.commit()
    conn.close()

def fake_sql_inj(type):
    conn = connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM types WHERE type = '{}'".format(type))
        conn.close()
        return True
    except Exception as e:
        conn.close()
        return False