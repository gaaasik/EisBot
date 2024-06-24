import sqlite3


def init_db():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS searches (
            search_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            search_active BOOLEAN,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_keywords (
            keyword_id INTEGER PRIMARY KEY,
            search_id INTEGER,
            keyword TEXT,
            FOREIGN KEY (search_id) REFERENCES searches (search_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_regions (
            region_id INTEGER PRIMARY KEY,
            search_id INTEGER,
            region TEXT,
            FOREIGN KEY (search_id) REFERENCES searches (search_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_price (
            price_id INTEGER PRIMARY KEY,
            search_id INTEGER,
            min_price INTEGER,
            max_price INTEGER,
            FOREIGN KEY (search_id) REFERENCES searches (search_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tenders (
            tender_id INTEGER PRIMARY KEY,
            details TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS favorite_tenders (
            favorite_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            tender_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (tender_id) REFERENCES tenders (tender_id)
        )
    ''')

    conn.commit()
    conn.close()


def add_user(user_id, username):
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username)
        VALUES (?, ?)
    ''', (user_id, username))

    conn.commit()
    conn.close()

# Additional database functions for adding searches, keywords, etc.