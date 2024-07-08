from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.all_handlers.another_function import Search_States,pages,all_regions,search_callback,current_page,selected_regions

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

