import sqlite3

from python.main_bot import *


# init_db(): инициализация базы данных и создание таблиц.
    # add_user(user_id, username, phone_number, message_count): добавление пользователя в базу данных.
    # add_search_filter(user_id, keyword, region, min_price, max_price): добавление фильтра поиска в базу данных.
    # add_tender(tender_id, tender_number, link, title, price): добавление тендера в базу данных.
    # add_favorite_tender(user_id, tender_id): добавление тендера в избранное пользователя.
    # get_user(user_id): получение информации о пользователе по его ID.
    # get_search_filters(user_id): получение всех фильтров поиска пользователя.
    # get_tenders(): получение всех тендеров.
    # get_favorite_tenders(user_id): получение всех избранных тендеров пользователя.
    # delete_search_filter(filter_id): удаление фильтра поиска по его ID.
    # delete_favorite_tender(user_id, tender_id): удаление тендера из избранного по ID пользователя и тендера.

def init_db():
    conn = sqlite3.connect('eisbot.db')
    cursor = conn.cursor()

    # Создание таблиц
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        phone_number TEXT,
        message_count INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS search_filters (
        filter_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        keyword TEXT,
        region TEXT,
        min_price REAL,
        max_price REAL,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tenders (
        tender_id INTEGER PRIMARY KEY,
        tender_number TEXT,
        link TEXT,
        title TEXT,
        price REAL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS favorite_tenders (
        user_id INTEGER,
        tender_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (tender_id) REFERENCES tenders (tender_id)
    )
    ''')

    conn.commit()
    conn.close()


def add_user(user_id, username, phone_number, message_count):
    conn = sqlite3.connect('eisbot.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT OR REPLACE INTO users (user_id, username, phone_number, message_count)
    VALUES (?, ?, ?, ?)
    ''', (user_id, username, phone_number, message_count))

    conn.commit()
    conn.close()


def add_search_filter(user_id, keyword, region, min_price, max_price):
    conn = sqlite3.connect('eisbot.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO search_filters (user_id, keyword, region, min_price, max_price)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, keyword, region, min_price, max_price))

    conn.commit()
    conn.close()
def add_keyword_in_db(user_id,keyword):
    conn = sqlite3.connect('eisbot.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO search_filters (user_id, keyword)
        VALUES (?, ?)
        ''', (user_id, keyword))

    conn.commit()
    conn.close()
# def add_regions(user_id,regions,all_region):
#     print("Пытаемяс добавить регионы")
#     conn = sqlite3.connect('eisbot.db')
#     cursor = conn.cursor()
#     if regions == all_region:
#         cursor.execute('''
#            INSERT INTO search_filters (user_id, region)
#            VALUES (?, ?)
#            ''', (user_id, regions))
#         conn.commit()
#         conn.close()





def add_tender(tender_id, tender_number, link, title, price):
    conn = sqlite3.connect('eisbot.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT OR REPLACE INTO tenders (tender_id, tender_number, link, title, price)
    VALUES (?, ?, ?, ?, ?)
    ''', (tender_id, tender_number, link, title, price))

    conn.commit()
    conn.close()


def add_favorite_tender(user_id, tender_id):
    conn = sqlite3.connect('eisbot.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO favorite_tenders (user_id, tender_id)
    VALUES (?, ?)
    ''', (user_id, tender_id))

    conn.commit()
    conn.close()


def get_user(user_id):
    conn = sqlite3.connect('eisbot.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM users WHERE user_id = ?
    ''', (user_id,))
    user = cursor.fetchone()

    conn.close()
    return user


def get_search_filters(user_id):
    conn = sqlite3.connect('eisbot.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM search_filters WHERE user_id = ?
    ''', (user_id,))
    filters = cursor.fetchall()

    conn.close()
    return filters


def get_tenders():
    conn = sqlite3.connect('eisbot.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT * FROM tenders
    ''')
    tenders = cursor.fetchall()

    conn.close()
    return tenders


def get_favorite_tenders(user_id):
    conn = sqlite3.connect('eisbot.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT tenders.* FROM tenders
    JOIN favorite_tenders ON tenders.tender_id = favorite_tenders.tender_id
    WHERE favorite_tenders.user_id = ?
    ''', (user_id,))
    favorite_tenders = cursor.fetchall()

    conn.close()
    return favorite_tenders


def delete_search_filter(filter_id):
    conn = sqlite3.connect('eisbot.db')
    cursor = conn.cursor()

    cursor.execute('''
    DELETE FROM search_filters WHERE filter_id = ?
    ''', (filter_id,))

    conn.commit()
    conn.close()


def delete_favorite_tender(user_id, tender_id):
    conn = sqlite3.connect('eisbot.db')
    cursor = conn.cursor()

    cursor.execute('''
    DELETE FROM favorite_tenders WHERE user_id = ? AND tender_id = ?
    ''', (user_id, tender_id))

    conn.commit()
    conn.close()
