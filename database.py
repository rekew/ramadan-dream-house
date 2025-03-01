import sqlite3 as sql
connection = sql.connect('users.db')
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT UNIQUE,
        username TEXT,
        quran_mark BOOLEAN,
        juz TEXT
    )
''')
connection.commit()

def clear_user_table():
    cursor.execute("UPDATE users SET juz = NULL, quran_mark = NULL")
    connection.commit()

def get_users():
    cursor.execute('SELECT telegram_id FROM users')
    users = [row[0] for row in cursor.fetchall()]
    return users

def get_taken_juz():
    cursor.execute("SELECT juz FROM users WHERE juz IS NOT NULL")
    return {row[0] for row in cursor.fetchall()}