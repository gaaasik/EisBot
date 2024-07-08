import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from bot.start_bot import dp,bot
from bot.database import database
from bot.all_handlers.another_function import Search_States,pages,all_regions,search_callback,current_page,selected_regions
from bot.keyboards.choose_region_keyboard import choose_regions
#



# @dp.message_handler(lambda message: message.text == "Поиск тендеров")
# async def add_search(message: types.Message):
#     await message.reply("Чтобы добавить поиск, заполните фильтры (необязательно):")
#     # Кнопки для добавления фильтров
#     inline_kb = InlineKeyboardMarkup()
#     inline_kb.add(
#         InlineKeyboardButton("Добавить ключевое поле", callback_data=search_callback.new(action="add_keyword")))
#     inline_kb.add(InlineKeyboardButton("Выбрать регион", callback_data=search_callback.new(action="select_region")))
#     inline_kb.add(
#         InlineKeyboardButton("Выбрать диапазон цен", callback_data=search_callback.new(action="select_price_range")))
#     inline_kb.add(
#         InlineKeyboardButton("Сохранить и начать поиск", callback_data=search_callback.new(action="save_and_search")))
#     await message.answer("Выберите опцию:", reply_markup=inline_kb)

# Функция для обработки выбора регионов

# @dp.message_handler(state=Search_States.keyword)
# async def process_keyword(message: types.Message, state: FSMContext):
#     keyword = message.text
#     database.add_keyword_in_db(message.from_user.id, keyword)
#     search_filters={'user_id': message.from_user.id,'keywords':keyword}
#
#     print(search_filters)
#
#     await message.reply("Ключевое слово "+keyword+" добавлено!")
#     inline_kb = InlineKeyboardMarkup()
#     inline_kb.add(InlineKeyboardButton("Выбрать регион", callback_data=search_callback.new(action="select_region")))
#     await message.reply(text="Выберете регион: ",reply_markup=choose_regions())
#     await state.finish()
#


# Обработчик нажатий на инлайн кнопки
@dp.callback_query_handler(lambda c: c.data.startswith('region_'))
async def process_region_selection(callback_query: types.CallbackQuery):
    print("обработка кнопок")
    try:
        page_num, index = map(int, callback_query.data.split('_')[1:])
        region = all_regions[page_num * 20 + index]  # Получаем выбранный регион
        selected_regions.append([region])

        print(f"Выбраные регионы: {selected_regions}")

        await bot.edit_message_text(
            text="Выберете регионы",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup= choose_regions()
        )
    except Exception as e:
        logging.error(f"Ошибка при обработке выбора региона: {e}")

# @dp.callback_query_handler(search_callback.filter(action="all_regions"))
# async def add_all_regions(call:types.CallbackQuery,callback_data:dict):
#     keyboard = InlineKeyboardMarkup("Сохранить и начать поиск", callback_data=search_callback.new(action="save_and_search"))
#     #     await message.answer("Выберите опцию:", reply_markup=)
#     await call.message.answer("Вы выбрали все регионы", reply_markup=keyboard)


# Обработчик нажатия на стрелки
@dp.callback_query_handler(lambda c: c.data.startswith(('prevRegion', 'nextRegion', 'pageRegion')))
async def process_page_change(callback_query: types.CallbackQuery):
    try:

        current_page = int(callback_query.data.split('_')[1])
        print(current_page)
        if callback_query.data.startswith('prevRegion'):
            current_page = max(0, current_page - 1)
        elif callback_query.data.startswith('nextRegion'):
            current_page = min(len(pages) - 1, current_page + 1)

        await bot.edit_message_text(
            text="Выберите регионssss:",
            chat_id=callback_query.message.chat.id,
            message_id=callback_query.message.message_id,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=pages[current_page])
        )
    except Exception as e:
        logging.error(f"Ошибка при переключении страниц: {e}")