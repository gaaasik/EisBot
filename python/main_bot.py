import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config
import database

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Command /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    database.add_user(message.from_user.id, message.from_user.username)
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Добавить поиск", callback_data='add_search'),
        InlineKeyboardButton("Мои поиски", callback_data='my_searches'),
        InlineKeyboardButton("Избранные тендеры", callback_data='favorite_tenders'),
        InlineKeyboardButton("Инструкция бота", callback_data='bot_instructions'),
        InlineKeyboardButton("Больше возможностей в будущем", callback_data='future_features', disabled=True)
    )
    await message.answer("Привет! Я бот для поиска тендеров. Выберите действие:", reply_markup=keyboard)

# Command /help or instructions
@dp.callback_query_handler(Text(equals='bot_instructions'))
async def bot_instructions(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Этот бот помогает искать тендеры по заданным параметрам...")

# Add search functionality
@dp.callback_query_handler(Text(equals='add_search'))
async def add_search(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Чтобы добавить поиск, заполните фильтры (необязательно):",
                           reply_markup=get_search_filters_keyboard())

# Additional handlers for 'my_searches', 'favorite_tenders', etc.

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
