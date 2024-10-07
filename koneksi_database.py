import sqlite3

def setup_database():
    with sqlite3.connect('sentimen.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS admin (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                nomor_hp TEXT NOT NULL,
                ig_link TEXT NOT NULL
            )
        ''')
        conn.commit()