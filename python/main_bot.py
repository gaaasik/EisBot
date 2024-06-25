print("версия 0.0")
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import config
import database

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


# FSM для управления состояниями
class SearchStates(StatesGroup):
    waiting_for_keyword = State()


# Список для хранения ключевых слов
user_keywords = {}

# Создание reply-клавиатуры для постоянного использования
reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
reply_keyboard.add(KeyboardButton("Поиск тендеров"), KeyboardButton("Мои тендеры"))
reply_keyboard.add(KeyboardButton("Больше возможностей"))
reply_keyboard.add(KeyboardButton("Помощь"), KeyboardButton("Обратная связь"))


# Приветственное сообщение с кнопкой "Начать поиск" и reply-кнопками
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    database.add_user(message.from_user.id, message.from_user.username)

    # Создание инлайн-кнопки "Начать поиск"
    inline_keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Начать поиск", callback_data='start_search')
    )

    await message.answer("Приветствую тебя. Ты готов начать работу?", reply_markup=inline_keyboard)
    await message.answer("Выберите опцию:", reply_markup=reply_keyboard)


# Обработчик для кнопки "Начать поиск"
@dp.callback_query_handler(Text(equals='start_search'))
async def start_search(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Чтобы добавить поиск, заполните фильтры (необязательно):",
                           reply_markup=get_search_filters_keyboard())


# Обработчики для кнопок фильтров поиска
@dp.callback_query_handler(Text(equals='add_keyword'))
async def add_keyword(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Введите ключевое слово для поиска:",
                           reply_markup=reply_keyboard)
    await SearchStates.waiting_for_keyword.set()


@dp.message_handler(state=SearchStates.waiting_for_keyword)
async def receive_keyword(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    keyword = message.text

    if user_id not in user_keywords:
        user_keywords[user_id] = []

    user_keywords[user_id].append(keyword)
    await message.answer(
        f"Ключевое слово '{keyword}' добавлено. Текущие ключевые слова: {', '.join(user_keywords[user_id])}",
        reply_markup=reply_keyboard)

    await state.finish()  # Завершаем текущее состояние


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
    # Здесь должна быть логика для выполнения поиска и возврата результатов


# Обработчик сообщений от кнопок reply
@dp.message_handler(lambda message: message.text in ["Поиск тендеров", "Мои тендеры", "Больше возможностей", "Помощь",
                                                     "Обратная связь"])
async def handle_reply_buttons(message: types.Message):
    if message.text == "Поиск тендеров":
        await message.answer("Функция 'Поиск тендеров' в разработке.", reply_markup=reply_keyboard)
    elif message.text == "Мои тендеры":
        await message.answer("Функция 'Мои тендеры' в разработке.", reply_markup=reply_keyboard)
    elif message.text == "Больше возможностей":
        await message.answer("Функция 'Больше возможностей' в разработке.", reply_markup=reply_keyboard)
    elif message.text == "Помощь":
        await message.answer("Функция 'Помощь' в разработке.", reply_markup=reply_keyboard)
    elif message.text == "Обратная связь":
        await message.answer("Функция 'Обратная связь' в разработке.", reply_markup=reply_keyboard)


# Существующая функция для получения клавиатуры фильтров поиска
def get_search_filters_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("Добавить ключевое поле", callback_data='add_keyword'),
        InlineKeyboardButton("Выбрать регион", callback_data='select_region'),
        InlineKeyboardButton("Выбрать диапазон цен", callback_data='select_price'),
        InlineKeyboardButton("Сохранить и начать поиск", callback_data='save_and_search')
    )
    return keyboard


# Error handling
@dp.errors_handler()
async def global_error_handler(update, exception):
    logging.exception(f'Update {update} caused error {exception}')
    return True


if __name__ == '__main__':
    database.init_db()
    executor.start_polling(dp, skip_updates=True)
