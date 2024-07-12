from aiogram import types

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_tender_message(tender_data, tender_number, total_tenders):
    message = (
        f"Тендер №{tender_number} из {total_tenders}\n"
        f"Объект закупки: {tender_data[3]}\n"
        f"Регион закупки: {tender_data[12]}\n"
        f"Начальная цена: {tender_data[4]}\n"
        f"Заказчик: {tender_data[5]}\n"
        f"Дата размещения: {tender_data[6]}\n"
        f"Дата окончания: {tender_data[7]}\n"
        f"Ссылка: {tender_data[2]}"
    )
    return message

# Функция для создания инлайн-клавиатуры с кнопками тендеров и навигации
def keyboard_to_show_tenders(listtender, selected_tender_index=None, page=1, page_size=5):
    # Определяем диапазон тендеров для отображения на текущей странице
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    current_tenders = listtender[start_index:end_index]

    # Создаем список кнопок для текущих тендеров
    buttons_tender = []
    for index, tender in enumerate(current_tenders):
        tender_number = start_index + index + 1
        button_text = f'Тендер {tender_number}'
        if selected_tender_index == tender_number:
            button_text += ' ✅'
        buttons_tender.append(types.InlineKeyboardButton(button_text, callback_data=f'tender_{tender_number}'))

    # Создаем инлайн-клавиатуру с кнопками для текущих тендеров
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons_tender)

    # Определяем количество страниц
    total_pages = (len(listtender) + page_size - 1) // page_size

    # Создаем кнопки для переключения страниц
    navigation_buttons = []
    if page > 1:
        navigation_buttons.append(types.InlineKeyboardButton('⬅️', callback_data=f'prev_page_tenders_{page - 1}'))
    navigation_buttons.append(types.InlineKeyboardButton(f'{page}/{total_pages}', callback_data='current_page'))
    if page < total_pages:
        navigation_buttons.append(types.InlineKeyboardButton('➡️', callback_data=f'next_page_tenders_{page + 1}'))

    # Добавляем кнопки навигации в клавиатуру
    keyboard.row(*navigation_buttons)

    return keyboard
