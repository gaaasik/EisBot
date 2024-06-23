import sqlite3
from telegram import Update
from telegram.ext import ContextTypes
# Создание соединения с базой данных
conn = sqlite3.connect('mydatabase.db')

# Создание курсора для выполнения запросов
cursor = conn.cursor()

# # Создание таблицы Users
# cursor.execute('''
# CREATE TABLE Users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     messages_count INTEGER
# )
# ''')
#
# # Создание таблицы saved_search
# cursor.execute('''
# CREATE TABLE saved_search (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     search_string TEXT NOT NULL
# )
# ''')
#
# # Сохранение изменений в базе данных
# conn.commit()

# Закрытие соединения
conn.close()


def add_user_to_db(update: Update) -> None:
    """
    Добавляет пользователя чат-бота в таблицу Users базы данных.

    Args:
        update: Объект Update, предоставляемый библиотекой telegram.ext.
        context: Объект Context, предоставляемый библиотекой telegram.ext.
    """

    # Получаем ID пользователя из объекта Update
    user_id = update.chat.id

    # Получаем имя пользователя из объекта Update
    print("сюда дошли")
    user_name = update.from_user.id
    # Подключаемся к базе данных
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    # Проверяем, есть ли уже пользователь в базе данных
    cursor.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
    existing_user = cursor.fetchone()

    # Если пользователь уже существует, обновляем количество сообщений
    if existing_user:
        cursor.execute("UPDATE Users SET messages_count = messages_count + 1 WHERE id = ?", (user_id,))
    # Если пользователь новый, добавляем его в таблицу
    else:
        cursor.execute("INSERT INTO Users (id, name, messages_count) VALUES (?, ?, 0)", (user_id, user_name))

    # Сохраняем изменения в базе данных
    conn.commit()
    # Закрываем соединение
    conn.close()

    # Вывод сообщения в чат (необязательно)
    update.message.reply_text(f"Привет, {user_name}! Я добавил тебя в свою базу данных.")
print('База данных создана с таблицами Users и saved_search')