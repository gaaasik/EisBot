from User import cursor, conn

print("ver2/0")
import logging
import parsing
from aiogram.utils.callback_data import CallbackData

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
import database
import parsing

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
storage = MemoryStorage()

# FSM для управления состояниями
class Search_States(StatesGroup):
    keyword = State()
    region = State()



# Список для хранения ключевых слов
user_keywords = {}

# Создание reply-клавиатуры для постоянного использования
reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
reply_keyboard.add(KeyboardButton("Поиск тендеров"))
reply_keyboard.add(KeyboardButton("Избранное"))
reply_keyboard.add(KeyboardButton("Больше возможностей"))
reply_keyboard.add(KeyboardButton("Помощь"), KeyboardButton("Обратная связь"))
#keyboard.add(InlineKeyboardButton("Сохранить и начать поиск", callback_data='save_and_search'))
search_callback = CallbackData("search", "action")

# Приветственное сообщение с кнопкой "Начать поиск" и reply-кнопками
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    database.add_user(message.from_user.id, message.from_user.username, "8917315038", 0)

    await message.answer(
        "Приветствую тебя! Знаешь ли ты, что на госзакупках можно найти самые необычные товары и услуги? Например, однажды был тендер на поставку папок для дарения. Давай начнем наш путь к успеху!",
        reply_markup=reply_keyboard)

    # Создание инлайн-кнопки "Начать поиск"
    start_find = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Начать поиск", callback_data='start_search')
    )
   # reply_keyboard.add(KeyboardButton("Поиск тендеров", callback_data='start_search'))

    await message.answer("Ты готов начать работу?", reply_markup=start_find)


# Функция для получения клавиатуры фильтров поиска
# def get_search_filters_keyboard(user_id):
#     keyboard = InlineKeyboardMarkup()
#     add_keyword_text = "Добавить ключевое поле"
#     add_region = "Выбрать регион"
#     add_price = "Выбрать диапазон цен"
#     if user_id in user_keywords and user_keywords[user_id]:
#         add_keyword_text += " ✅"
#         add_price +=" ✅"
#     keyboard.add(InlineKeyboardButton(add_keyword_text, callback_data='add_keyword'))
#     keyboard.add(InlineKeyboardButton(add_region, callback_data='select_region'))
#     keyboard.add(InlineKeyboardButton(add_price, callback_data='select_price'))
#     keyboard.add(InlineKeyboardButton("Сохранить и начать поиск", callback_data='save_and_search'))
#
#     return keyboard
#

# Обработчик для кнопок "Начать поиск" и "Добавить поиск"
@dp.callback_query_handler(Text(equals=['start_search', 'add_search']))
@dp.message_handler(lambda message: message.text == "Поиск тендеров")
async def add_search(message: types.Message):
    await message.reply("Чтобы добавить поиск, заполните фильтры (необязательно):")

    # Кнопки для добавления фильтров
    inline_kb = InlineKeyboardMarkup()
    inline_kb.add(
        InlineKeyboardButton("Добавить ключевое поле", callback_data=search_callback.new(action="add_keyword")))
    inline_kb.add(InlineKeyboardButton("Выбрать регион", callback_data=search_callback.new(action="select_region")))
    inline_kb.add(
        InlineKeyboardButton("Выбрать диапазон цен", callback_data=search_callback.new(action="select_price_range")))
    inline_kb.add(
        InlineKeyboardButton("Сохранить и начать поиск", callback_data=search_callback.new(action="save_and_search")))
    await message.answer("Выберите опцию:", reply_markup=inline_kb)

# Обработка инлайн-кнопок
@dp.callback_query_handler(search_callback.filter(action="add_keyword"))
async def add_keyword_callback(call: types.CallbackQuery, callback_data: dict):
    await call.message.answer("Введите ключевое слово для поиска:")
    await Search_States.keyword.set()

@dp.message_handler(state=Search_States.keyword)
async def process_keyword(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    print("зашли23")
    keyword = message.text
    cursor.execute('''
    INSERT INTO search_filters (user_id, keywords) VALUES (?, ?)
    ''', (user_id, keyword))
    conn.commit()
    await state.finish()
    await message.reply("Ключевое слово добавлено!")
@dp.message_handler(state=Search_States.keyword)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        print("pfikb2")
        data['Keyword'] = message.text
        await Search_States.next()
        await message.reply("Выберете регион")







@dp.callback_query_handler(Text(equals='select_region'))
async def select_region(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Выберите регион для поиска:", reply_markup=reply_keyboard)


@dp.callback_query_handler(Text(equals='select_price'))
async def select_price(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите диапазон цен для поиска:", reply_markup=reply_keyboard)


@dp.callback_query_handler(Text(equals='save_and_search'))
async def save_and_search(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Ваши параметры сохранены. Начинаем поиск...",
                           reply_markup=reply_keyboard)
    user_id = callback_query.from_user.id
    # Получение данных из базы данных (нужно будет реализовать)
    keywords = ...
    regions = ...
    min_price = ...
    max_price = ...
    # Сохранение фильтров поиска в базе данных


    cursor.execute('''
    INSERT INTO search_filters (user_id, keywords, regions, min_price, max_price)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, keywords, regions, min_price, max_price))
    conn.commit()
    #await call.message.answer("Фильтры сохранены. Начинаем поиск...")
    await bot.send_message(callback_query.from_user.id, text = "Тут результат парсинга")
    listender = parsing.parse_zakupki("1")
    await bot.send_message(callback_query.from_user.id,listender, reply_markup=reply_keyboard)


# Обработчик сообщений от кнопок reply
@dp.message_handler(
    lambda message: message.text in ["Поиск тендеров", "Мои тендеры", "Избранное", "Больше возможностей", "Помощь",
                                     "Обратная связь"])
async def handle_reply_buttons(message: types.Message):
    # if message.text == "Поиск тендеров":
    #     print("z nen")
    #     await  bot.send_message(message.from_user.id, "Чтобы добавить поиск, заполните фильтры (необязательно):", reply_markup=get_search_filters_keyboard(message.from_user.id))
    if message.text == "Мои тендеры":
        await message.answer("Скоро добавим.", reply_markup=reply_keyboard)
    elif message.text == "Избранное":
        await message.answer("Тут скоро будут отображаться ваши сохраненные тендеры.", reply_markup=reply_keyboard)
    elif message.text == "Больше возможностей":
        await message.answer(
            "Больше возможностей в платной версии. Полезные функции, которые вы можете добавить:\n- Автоматическое уведомление о новых тендерах\n- Фильтрация по более детальным параметрам\n- Сохранение и экспорт результатов поиска\n- Аналитика и отчеты по тендерам",
            reply_markup=reply_keyboard)
    elif message.text == "Помощь":
        await message.answer("Функция 'Помощь' в разработке.", reply_markup=reply_keyboard)
    elif message.text == "Обратная связь":
        await message.answer("Функция 'Обратная связь' в разработке.", reply_markup=reply_keyboard)


# Error handling
@dp.errors_handler()
async def global_error_handler(update, exception):
    logging.exception(f'Update {update} caused error {exception}')
    return True


if __name__ == '__main__':
    database.init_db()
    executor.start_polling(dp, skip_updates=True)
