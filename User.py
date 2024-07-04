import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler
)

# Callback data для кнопок
CALLBACK_FILL_FIELDS = "fill_fields"
CALLBACK_CHOOSE_REGION = "choose_region"
CALLBACK_CHOOSE_PRICE = "choose_price"
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn



# Создаем соединение с БД (или файл, если его нет)
conn = create_connection('search_bot.db')
cursor = conn.cursor()

# Создаем таблицы, если их нет
cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                    id INTEGER PRIMARY KEY, 
                    name TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS SearchData (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    keyword TEXT,
                    region TEXT DEFAULT NULL,
                    price_range TEXT DEFAULT NULL,
                    FOREIGN KEY (user_id) REFERENCES Users(id))''')
conn.commit()



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение и начальную клавиатуру."""
    keyboard = [
        [InlineKeyboardButton("Начать поиск 🔎", callback_data="start_search")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Привет! Я помогу тебе с поиском. ", reply_markup=reply_markup
    )

async def start_search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет сообщение с выбором фильтров."""
    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Заполнить поля поиска", callback_data=CALLBACK_FILL_FIELDS)],
        [InlineKeyboardButton("Выбрать регион поиска", callback_data=CALLBACK_CHOOSE_REGION)],
        [InlineKeyboardButton("Выбрать диапазон цен", callback_data=CALLBACK_CHOOSE_PRICE)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Заполните фильтры поиска:", reply_markup=reply_markup)


async def handle_keyword(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает ввод ключевого слова и сохраняет его в БД."""
    user_input = update.message.text
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    # Добавляем пользователя в таблицу Users, если его там нет
    cursor.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
    existing_user = cursor.fetchone()
    if not existing_user:
        cursor.execute("INSERT INTO Users (id, name) VALUES (?, ?)", (user_id, user_name))
        conn.commit()

    # Сохраняем ключевое слово в таблицу SearchData
    cursor.execute("INSERT INTO SearchData (user_id, keyword) VALUES (?, ?)", (user_id, user_input))
    conn.commit()
    await update.message.reply_text(f"Ключевое слово '{user_input}' сохранено!")




async def handle_fill_fields(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Запрашивает ввод ключевого слова."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("Введите ключевое слово для поиска:")

    # Регистрируем обработчик текстового сообщения для получения ключевого слова
    context.user_data['waiting_for_keyword'] = True
    #context.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_keyword), group=1)
print("Остановились тут ")




async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает нажатия на inline-кнопки."""
    query = update.callback_query
    await query.answer()

    if query.data == CALLBACK_FILL_FIELDS:
        await handle_fill_fields(update, context)
    elif query.data == CALLBACK_CHOOSE_REGION:
        # Здесь будет логика выбора региона (аналогично handle_fill_fields)
        await query.edit_message_text("Функция выбора региона в разработке.")
    elif query.data == CALLBACK_CHOOSE_PRICE:
        # Здесь будет логика выбора диапазона цен (аналогично handle_fill_fields)
        await query.edit_message_text("Функция выбора диапазона цен в разработке.")


def main() -> None:
    """Запускает бота."""
    application = Application.builder().token("YOUR_BOT_TOKEN").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback_query))
    application.run_polling()


if __name__ == "__main__":
    main()


# import sqlite3
# from telegram import Update
# from telegram.ext import ContextTypes
# # Создание соединения с базой данных
# conn = sqlite3.connect('mydatabase.db')
#
# # Создание курсора для выполнения запросов
# cursor = conn.cursor()
#
# # # Создание таблицы Users
# # cursor.execute('''
# # CREATE TABLE Users (
# #     id INTEGER PRIMARY KEY AUTOINCREMENT,
# #     name TEXT NOT NULL,
# #     messages_count INTEGER
# # )
# # ''')
# #
# # # Создание таблицы saved_search
# # cursor.execute('''
# # CREATE TABLE saved_search (
# #     id INTEGER PRIMARY KEY AUTOINCREMENT,
# #     search_string TEXT NOT NULL
# # )
# # ''')
# #
# # # Сохранение изменений в базе данных
# # conn.commit()
#
# # Закрытие соединения
# conn.close()
#
#
# def add_user_to_db(update: Update) -> None:
#     """
#     Добавляет пользователя чат-бота в таблицу Users базы данных.
#
#     Args:
#         update: Объект Update, предоставляемый библиотекой telegram.ext.
#         context: Объект Context, предоставляемый библиотекой telegram.ext.
#     """
#
#     # Получаем ID пользователя из объекта Update
#     user_id = update.chat.id
#
#     # Получаем имя пользователя из объекта Update
#     print("сюда дошли")
#     user_name = update.from_user.id
#     # Подключаемся к базе данных
#     conn = sqlite3.connect('mydatabase.db')
#     cursor = conn.cursor()
#
#     # Проверяем, есть ли уже пользователь в базе данных
#     cursor.execute("SELECT * FROM Users WHERE id = ?", (user_id,))
#     existing_user = cursor.fetchone()
#
#     # Если пользователь уже существует, обновляем количество сообщений
#     if existing_user:
#         cursor.execute("UPDATE Users SET messages_count = messages_count + 1 WHERE id = ?", (user_id,))
#     # Если пользователь новый, добавляем его в таблицу
#     else:
#         cursor.execute("INSERT INTO Users (id, name, messages_count) VALUES (?, ?, 0)", (user_id, user_name))
#
#     # Сохраняем изменения в базе данных
#     conn.commit()
#     # Закрываем соединение
#     conn.close()
#
#     # Вывод сообщения в чат (необязательно)
#     #update.message.reply_text(f"Привет, {user_name}! Я добавил тебя в свою базу данных.")
# print('База данных создана с таблицами Users и saved_search')
# print(mydata)