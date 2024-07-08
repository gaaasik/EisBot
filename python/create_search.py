import logging

from main_bot import FSMContext

import database
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters import Text
from bot.keyboards.choose_region_keyboard import choose_regions
selected_regions=[]

# Функция для обработки выбора регионов
# def choose_regions():
#       # Здесь должны быть все регионы
#
#
#     print("формируем кнопки")
#     inline_keyboard = []
#     for page_num, page in enumerate(pages):
#         rows = []
#         for i in range(0, len(page), 2):
#             row = [InlineKeyboardButton(page[i], callback_data=f'region_{page_num}_{i}')]
#             if i + 1 < len(page):
#                 row.append(InlineKeyboardButton(page[i + 1], callback_data=f'region_{page_num}_{i + 1}'))
#             rows.append(row)
#         # Добавляем стрелки переключения страниц
#         rows.append([
#             InlineKeyboardButton("⏪", callback_data=f'prevRegion_{page_num}'),
#             InlineKeyboardButton(f"{page_num + 1}/{len(pages)}", callback_data=f'pageRegion_{page_num}'),
#             InlineKeyboardButton("⏩", callback_data=f'nextRegion_{page_num}')
#         ])
#         rows.append([InlineKeyboardButton("Выбрать все регионы", callback_data='all_regions')])
#         inline_keyboard.append(rows)
#
#     # Отображаем первую страницу
#     return InlineKeyboardMarkup(inline_keyboard=inline_keyboard[current_page])

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