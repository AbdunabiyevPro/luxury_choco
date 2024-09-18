import sqlite3
import psycopg2

def init_db():
    conn = sqlite3.connect("../bot_users.db")
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            chat_id INTEGER NOT NULL,
            latitude REAL,
            longitude REAL,
            phone_number TEXT
        );
    ''')

    conn.commit()
    conn.close()


def products():
    conn = sqlite3.connect("../bot_users.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        stock INTEGER DEFAULT 0,
        country TEXT,
        image_path TEXT

        )
    ''')

    conn.commit()

    conn.close()

def admin():
    conn = sqlite3.connect("../bot_users.db")
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admins(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        name TEXT
    )
    ''')
    conn.commit()
    conn.close()

admin()
products()
init_db()
