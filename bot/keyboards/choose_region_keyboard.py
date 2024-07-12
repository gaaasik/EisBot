from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from bot.all_handlers.another_function import Search_States,pages,all_regions,search_callback,current_page,selected_regions
import bot.all_handlers.create_search_filters.create_search
from bot.start_bot import dp

search_callback = CallbackData("search", "action")
async def choose_regions():
    # Здесь должны быть все регионы

    print("формируем кнопки")
    inline_keyboard = []
    for page_num, page in enumerate(pages):
        rows = []
        for i in range(0, len(page), 2):
            row = [InlineKeyboardButton(page[i], callback_data=f'region_{page_num}_{i}')]
            if i + 1 < len(page):
                row.append(InlineKeyboardButton(page[i + 1], callback_data=f'region_{page_num}_{i + 1}'))
            rows.append(row)
        # Добавляем стрелки переключения страниц
        rows.append([
            InlineKeyboardButton("⏪", callback_data=f'prevRegion_{page_num}'),
            InlineKeyboardButton(f"{page_num + 1}/{len(pages)}", callback_data=f'pageRegion_{page_num}'),
            InlineKeyboardButton("⏩", callback_data=f'nextRegion_{page_num}')
        ])
        rows.append([InlineKeyboardButton("Выбрать все регионы", callback_data='all_regions')])
        inline_keyboard.append(rows)

    # Отображаем первую страницу
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard[current_page])


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'all_regions')
async def add_all_regions(callback_query: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup("Сохранить и начать поиск", callback_data=search_callback.new(action="save_and_search"))
    #     await message.answer("Выберите опцию:", reply_markup=)
    await callback_query.message.answer("Вы выбрали все регионы", reply_markup=keyboard)
