#from User import cursor, conn
print("ver2.0.12")

from create_search import*
print("ver2.0.12")
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
bot = Bot(token=config.API_TOKEN)
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
reply_keyboard.add(KeyboardButton("ПАРСИНГ (Временная кнопка)"))
reply_keyboard.add(KeyboardButton("Избранное"))
reply_keyboard.add(KeyboardButton("Больше возможностей"))
reply_keyboard.add(KeyboardButton("Помощь"), KeyboardButton("Обратная связь"))
save_and_search_btn =  (InlineKeyboardButton(text="Сохранить и начать поиск", callback_data='save_and_search'))
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
#@dp.callback_query_handler(Text(equals=['start_search', 'add_search']))


@dp.callback_query_handler(Text(equals='start_search'))
async def add_search(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Чтобы добавить поиск, введите ключевое поле для поиска : ")
    await Search_States.keyword.set()
@dp.message_handler(lambda message: message.text == "Поиск тендеров")
async def add_search(message: types.Message):
    await message.reply("Чтобы добавить поиск, введите ключевое поле для поиска : ")
    await Search_States.keyword.set()

    # Кнопки для добавления фильтров

    # inline_kb.add(
    #     InlineKeyboardButton("Добавить ключевое поле", callback_data=search_callback.new(action="add_keyword")))
    #
    # inline_kb.add(
    #     InlineKeyboardButton("Выбрать диапазон цен", callback_data=search_callback.new(action="select_price_range")))
    # inline_kb.add(
    #     InlineKeyboardButton("Сохранить и начать поиск", callback_data=search_callback.new(action="save_and_search")))
    #await message.answer("Выберите опцию:", reply_markup=inline_kb)


# # Обработка инлайн-кнопок
# @dp.callback_query_handler(search_callback.filter(action="add_keyword"))
# async def add_keyword_callback(call: types.CallbackQuery, callback_data: dict):
#     await call.message.answer("Введите ключевое слово для поиска:")
#     await Search_States.keyword.set()
#



@dp.message_handler(state=Search_States.keyword)
async def process_keyword(message: types.Message, state: FSMContext):
    keyword = message.text
    database.add_keyword_in_db(message.from_user.id, keyword)
    search_filters={'user_id': message.from_user.id,'keywords':keyword}

    print(search_filters)

    await message.reply("Ключевое слово "+keyword+" добавлено!")
    inline_kb = InlineKeyboardMarkup()
    inline_kb.add(InlineKeyboardButton("Выбрать регион", callback_data=search_callback.new(action="select_region")))
    await message.reply(text="Выберете регион: ",reply_markup=choose_regions())
    await state.finish()

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


# @dp.message_handler(state=Search_States.region)
# async def process_keyword(message: types.Message, state: FSMContext):
#     select_region = message.text
#     print(select_region)
#     await state.finish()
# @dp.message_handler(state=Search_States.keyword)
# async def process_name(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         print("pfikb2")
#         data['Keyword'] = message.text
#         await Search_States.next()
#         await message.reply("Выберете регион")
#


# Обработчик нажатий на инлайн кнопки
@dp.callback_query_handler(lambda c: c.data.startswith('region_'))
async def process_region_selection(callback_query: types.CallbackQuery):
    print("обработка кнопок")
    try:
        page_num, index = map(int, callback_query.data.split('_')[1:])
        region = all_regions[page_num * 20 + index]  # Получаем выбранный регион
        selected_regions = [region]

        print(f"Выбраные регионы: {selected_regions}")

        await bot.edit_message_text(
            text="Регион выбран",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup= choose_regions()
        )
    except Exception as e:
        logging.error(f"Ошибка при обработке выбора региона: {e}")


# Обработчик нажатия на стрелки
@dp.callback_query_handler(lambda c: c.data.startswith(('prev', 'next', 'page')))
async def process_page_change(callback_query: types.CallbackQuery):
    try:
        print("кнопка")
        current_page = int(callback_query.data.split('_')[1])

        if callback_query.data.startswith('prev'):
            current_page = max(0, current_page - 1)
        elif callback_query.data.startswith('next'):
            current_page = min(len(pages) - 1, current_page + 1)

        await bot.edit_message_text(
            text="Выберите регион:",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=pages[current_page])
        )
    except Exception as e:
        logging.error(f"Ошибка при переключении страниц: {e}")

@dp.callback_query_handler(Text(equals='all_regions'))
async def select_all_regions(callback_query: types.CallbackQuery):
    print("все регионы")
    save_and_search_btn = InlineKeyboardMarkup().add(
        InlineKeyboardButton("Сохранить и начать поиск", callback_data='save_and_search')
    )
    await callback_query.message.answer("Вы выбрали все регионы",reply_markup=save_and_search_btn)


    print("добавили в db")


@dp.message_handler(lambda message: message.text == "ПАРСИНГ (Временная кнопка)")
async def save_and_search_unusal(message: types.Message):
     await message.answer("Начинаем поиск...")  #user_id = bot.message.from_user.id
    # Получение данных из базы данных (нужно будет реализовать)
    # Сохранение фильтров поиска в базе данных



     listender = database.get_tenders()

     for item in listender:
         print(item)
         await message.answer(str(item))



@dp.callback_query_handler(Text(equals='save_and_search'))
async def save_and_search(callback_query: types.CallbackQuery):
    print("Сохраняем поиск")

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Ваши параметры сохранены. Начинаем поиск...",
                           reply_markup=reply_keyboard)
    user_id = callback_query.from_user.id
    # Получение данных из базы данных (нужно будет реализовать)
    # Сохранение фильтров поиска в базе данных

    #database.add_regions()
    #await call.message.answer("Фильтры сохранены. Начинаем поиск...")
    await bot.send_message(callback_query.from_user.id, text = "Тут результат парсинга")

    listender = database.get_tenders()

    print(listender)
    for item in listender:

        await bot.send_message(callback_query.from_user.id,text = str(item))



# Error handling
@dp.errors_handler()
async def global_error_handler(update, exception):
    logging.exception(f'Update {update} caused error {exception}')
    print("Какая то ошибка")
    return True


if __name__ == '__main__':
    database.init_db()
    executor.start_polling(dp, skip_updates=True)
