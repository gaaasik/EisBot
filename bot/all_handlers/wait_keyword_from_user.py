import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from bot.start_bot import dp,bot
from bot.all_handlers.another_function import Search_States
from bot.database.database import add_keyword_in_db
from bot.keyboards.choose_region_keyboard import choose_regions

search_callback = CallbackData("search", "action")
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
pages = [all_regions[i:i + 20] for i in range(0, len(all_regions), 20)]  # Формируем страницы по 20 регионов



@dp.message_handler(state=Search_States.keyword)
async def process_keyword(message: types.Message, state: FSMContext):
    keyword = message.text
    add_keyword_in_db(message.from_user.id, keyword)
    search_filters={'user_id': message.from_user.id,'keywords':keyword}

    print(search_filters)

    await message.reply("Ключевое слово "+keyword+" добавлено!")
    inline_kb = InlineKeyboardMarkup()
    inline_kb.add(InlineKeyboardButton("Выбрать регион", callback_data=search_callback.new(action="select_region")))
    list = await choose_regions()
    await message.reply(text="Выберете регион: ",reply_markup=list)
    await state.finish()

