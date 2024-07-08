#from User import cursor, conn
print("ver2.0")


import logging

from aiogram.utils.callback_data import CallbackData
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
# from aiogram.dispatcher.filters import Text, state
# from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.config_bot import config_bot
from bot.database import database

all_regions = ["г. Москва", "Белгородская область",
               "Брянская область",
               "Владимирская область",
               "Воронежская область",
               "Ивановская область",
               "Калужская область",
               "Костромская область",
               "Курская область",
               "Липецкая область",
               "Московская область",
               "Орловская область",
               "Рязанская область",
               "Смоленская область",
               "Тамбовская область",
               "Тверская область",
               "Тульская область",
               "Ярославская область",

               "Республика Карелия",
               "Республика Коми",
               "Архангельская область",
               "Ненецкий автономный округ",
               "Вологодская область",
               "Калининградская область",
               "Ленинградская область",
               "Мурманская область",
               "Новгородская область",
               "Псковская область",
               "г. Санкт-Петербург",
               "Республика Адыгея",
               "Республика Дагестан",
               "Республика Ингушетия",
               "Кабардино-Балкарская Республика",
               "Республика Калмыкия",
               "Карачаево-Черкесская Республика",
               "Республика Северная Осетия - Алания",
               "Чеченская Республика",
               "Краснодарский край",
               "Ставропольский край",
               "Астраханская область",
               "Волгоградская область",
               "Ростовская область",

               "Республика Башкортостан",
               "Республика Марий Эл",
               "Республика Мордовия",
               "Республика Татарстан",
               "Удмуртская Республика",
               "Чувашская Республика",
               "Пермский край",
               "Кировская область",
               "Нижегородская область",
               "Оренбургская область",
               "Пензенская область",
               "Самарская область",
               "Саратовская область",
               "Ульяновская область",
               "Курганская область",
               "Свердловская область",
               "Тюменская область",
               "Ханты-Мансийский автономный округ - Югра",
               "Ямало-Ненецкий автономный округ",
               "Челябинская область",

               "Республика Алтай",
               "Республика Бурятия",
               "Республика Тыва",
               "Республика Хакасия",
               "Алтайский край",
               "Красноярский край",
               "Иркутская область",

               "Кемеровская область",
               "Новосибирская область",
               "Омская область",
               "Томская область",
               "Читинская область",


               "Республика Саха (Якутия)",
               "Камчатский край",
               "Приморский край",
               "Хабаровский край",
               "Амурская область",
               "Магаданская область",
               "Сахалинская область",
               "Еврейская автономная область",
               "Чукотский автономный округ"]
current_page = 0
pages = [all_regions[i:i + 20] for i in range(0, len(all_regions), 20)]  # Формируем страницы по 20 регионов
selected_region = None
items_per_page = 20
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=config_bot.API_TOKEN)
dp = Dispatcher(bot,storage=storage)
dp.middleware.setup(LoggingMiddleware())
#search_filters_dict={}

# FSM для управления состояниями
class Search_States(StatesGroup):
    keyword = State()



# Список для хранения ключевых слов
user_keywords = {}

# Создание reply-клавиатуры для постоянного использования
reply_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
reply_keyboard.add(KeyboardButton("Поиск тендеров"))
reply_keyboard.add(KeyboardButton("Показать найденные тендера (Временная кнопка)"))
reply_keyboard.add(KeyboardButton("Избранное"))
reply_keyboard.add(KeyboardButton("Больше возможностей"))
reply_keyboard.add(KeyboardButton("Помощь"), KeyboardButton("Обратная связь"))
save_and_search_btn =  (InlineKeyboardButton(text="Сохранить и начать поиск", callback_data='save_and_search'))
search_callback = CallbackData("search", "action")

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
    await message.answer("Ты готов начать работу?", reply_markup=start_find)



if __name__ == '__main__':
    database.init_db()
    executor.start_polling(dp, skip_updates=True)
