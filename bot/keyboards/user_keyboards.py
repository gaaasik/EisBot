from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from aiogram.filters.callback_data import CallbackData

from aiogram.types import  InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

def create_start_ReplyKeyboardMarkup():

    # Список для хранения ключевых слов
    user_keywords = {}

    # Создание reply-клавиатуры для постоянного использования
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_keyboard.add(KeyboardButton("Поиск тендеров"))
    reply_keyboard.add(KeyboardButton("Показать найденные тендера (Временная кнопка)"))
    reply_keyboard.add(KeyboardButton("Избранное"))
    reply_keyboard.add(KeyboardButton("Больше возможностей"))
    reply_keyboard.add(KeyboardButton("Помощь"), KeyboardButton("Обратная связь"))
    return reply_keyboard
