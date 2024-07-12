from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData

from bot.database.database import get_tenders
from bot.keyboards.showTendersInMessage import keyboard_to_show_tenders, create_tender_message
from bot.parsing.parsing import get_page
from bot.start_bot import dp, bot
search_callback = CallbackData("search", "action")


def create_start_ReplyKeyboardMarkup():
    # Список для хранения ключевых слов
    user_keywords = {}

    # Создание reply-клавиатуры для постоянного использования
    reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    reply_keyboard.add(KeyboardButton("Создать новый поиск"))
    reply_keyboard.add(KeyboardButton("Показать найденные тендера (Временная кнопка)"))
    reply_keyboard.add(KeyboardButton("Избранное"))
    reply_keyboard.add(KeyboardButton("Больше возможностей"))
    reply_keyboard.add(KeyboardButton("Помощь"), KeyboardButton("Обратная связь"))
    return reply_keyboard

@dp.message_handler(lambda message: message.text == "Показать найденные тендера (Временная кнопка)")
async def handle_reply_buttons(message: types.Message):
    get_page(
        url='https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=%D0%BC%D0%B0%D1%80%D0%BA%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5+%D0%BA%D0%BE%D0%BD%D0%B2%D0%B5%D1%80%D1%82%D1%8B&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&priceFromGeneral=100000&currencyIdGeneral=-1')
    print("парсинг запустиля")
    listtender = get_tenders()  # Получаем список тендеров из базы данных

    if not listtender:
        await message.answer("Нет доступных тендеров.")
        return

    keyboard = keyboard_to_show_tenders(listtender)
    message_text = create_tender_message(listtender[0], 1, len(listtender))
    await message.answer(message_text, reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Избранное")
async def handle_reply_buttons(message: types.Message):
    await message.answer("Функция 'Избранное' в разработке.",
                         reply_markup=create_start_ReplyKeyboardMarkup())

@dp.message_handler(lambda message: message.text == "Больше возможностей")
async def handle_reply_buttons(message: types.Message):
    await message.answer("Функция 'Больше возможностей' в разработке.",
                         reply_markup=create_start_ReplyKeyboardMarkup())

@dp.message_handler(lambda message: message.text == "Помощь")
async def handle_reply_buttons(message: types.Message):
    await message.answer("Функция 'Помощь' в разработке.",
                         reply_markup=create_start_ReplyKeyboardMarkup())

@dp.message_handler(lambda message: message.text == "Обратная связь")
async def handle_reply_buttons(message: types.Message):
    await message.answer("Функция 'Обратная связь' в разработке.", reply_markup=create_start_ReplyKeyboardMarkup())
