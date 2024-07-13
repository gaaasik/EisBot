

import logging
from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.utils.callback_data import CallbackData

from bot.database.database import add_user, get_tenders
from bot.parsing.parsing import get_page
from bot.keyboards.showTendersInMessage import keyboard_to_show_tenders,create_tender_message
from bot.keyboards.create_reply_keyboard import create_start_ReplyKeyboardMarkup
from bot.start_bot import dp,bot
from aiogram.dispatcher import FSMContext
# FSM для управления состояниями

search_callback = CallbackData("search", "action")
class Search_States(StatesGroup):
    keyword = State()

# pages = [all_regions[i:i + 20] for i in range(0, len(all_regions), 20)]  # Формируем страницы по 20 регионов
selected_region = None
items_per_page = 20
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    add_user(message.from_user.id, message.from_user.username, "8917315038", 0)

    await message.answer(
        "Приветствую тебя! Знаешь ли ты, что на госзакупках можно найти самые необычные товары и услуги? Например, однажды был тендер на поставку папок для дарения. Давай начнем наш путь к успеху!",
        reply_markup=create_start_ReplyKeyboardMarkup())

    # Создание инлайн-кнопки "Начать поиск"
    start_find = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Начать поиск", callback_data='start_search')
    )
    await message.answer("Ты готов начать работу?", reply_markup=start_find)

# @dp.message_handler(lambda message: message.text == "Показать найденные тендера (Временная кнопка)")
# async def save_and_search_unusal(message: types.Message):
#     get_page(
#         url='https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=%D0%BC%D0%B0%D1%80%D0%BA%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5+%D0%BA%D0%BE%D0%BD%D0%B2%D0%B5%D1%80%D1%82%D1%8B&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&priceFromGeneral=100000&currencyIdGeneral=-1')
#     print("парсинг запустиля")
#     listtender = get_tenders()  # Получаем список тендеров из базы данных
#
#     if not listtender:
#         await message.answer("Нет доступных тендеров.")
#         return
#
#     keyboard = keyboard_to_show_tenders(listtender)
#     message_text = create_tender_message(listtender[0], 1, len(listtender))
#     await message.answer(message_text, reply_markup=keyboard)
@dp.callback_query_handler(Text(equals='save_and_search'))
async def save_and_search(callback_query: types.CallbackQuery):
    print("Сохраняем поиск")
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Ваши параметры сохранены. Начинаем поиск...",
                           reply_markup=create_start_ReplyKeyboardMarkup())
    user_id = callback_query.from_user.id
   # create_search_filters() #создание таблицы поиска


    get_page(url='https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=%D0%BC%D0%B0%D1%80%D0%BA%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5+%D0%BA%D0%BE%D0%BD%D0%B2%D0%B5%D1%80%D1%82%D1%8B&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&priceFromGeneral=100000&currencyIdGeneral=-1')

    # Получение данных из базы данных (нужно будет реализовать)

    # Сохранение фильтров поиска в базе данных

    await bot.send_message(callback_query.from_user.id, text = "Тут результат парсинга")

    listender = get_tenders()

    await bot.send_message(callback_query.from_user.id, text = "")

    print(listender)
    for item in listender:

        await bot.send_message(callback_query.from_user.id,text = str(item))



# Обработчик команды /show_tenders для отображения первой страницы с тендерами
# Обработчик для команды /show_tenders


# Error handling
@dp.errors_handler()
async def global_error_handler(update, exception):
    logging.exception(f'Update {update} caused error {exception}')
    print("Какая то ошибка")
    return True
