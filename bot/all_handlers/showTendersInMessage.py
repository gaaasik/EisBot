


from aiogram import types
from aiogram.dispatcher import FSMContext

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.database.database import get_tenders
from bot.keyboards.showTendersInMessage import keyboard_to_show_tenders, create_tender_message
from bot.start_bot import dp, bot

#Отображение найденных тендеров
@dp.message_handler(commands=['show_tenders'])
async def show_tenders(message: types.Message):
    listtender = get_tenders()  # Получаем список тендеров из базы данных

    if not listtender:
        await message.answer("Нет доступных тендеров.")
        return

    keyboard = keyboard_to_show_tenders(listtender)
    message_text = create_tender_message(listtender[0], 1, len(listtender))
    await message.answer(message_text, reply_markup=keyboard)

# Обработчик для нажатия на кнопки навигации по страницам и выбора тендеров
@dp.callback_query_handler(lambda c: c.data and (c.data.startswith('prev_page_tenders') or c.data.startswith('next_page_tenders') or c.data.startswith('tender_')))
async def process_page_navigation(callback_query: types.CallbackQuery, state: FSMContext):
    listtender = get_tenders()  # Получаем список тендеров
    action = callback_query.data.split('_')[0]

    # Инициализация переменной current_page
    current_page = 1

    # Проверка нажатия на кнопку выбора тендера
    if action == 'tender':
        print("тендер")
        selected_tender_index = int(callback_query.data.split('_')[1])
        selected_tender = listtender[selected_tender_index - 1]  # Выбираем данные выбранного тендера
        current_page = (selected_tender_index - 1) // 5 + 1  # Определяем текущую страницу
        keyboard = keyboard_to_show_tenders(listtender, selected_tender_index, page=current_page)
        message_text = create_tender_message(selected_tender, selected_tender_index, len(listtender))
    else:
        # Обработка кнопок навигации
        if callback_query.data.startswith('prev_page_tenders'):
            print("стрелка1")
            current_page = int(callback_query.data.split('_')[3])
            print(current_page)

        elif callback_query.data.startswith('next_page_tenders'):
            print("стрелка")
            current_page = int(callback_query.data.split('_')[3])
            print(current_page)

        total_pages = (len(listtender) + 4) // 5  # Определяем общее количество страниц

        if current_page < 1 or current_page > total_pages:
            await bot.answer_callback_query(callback_query.id, text="Недопустимая страница.", show_alert=True)
            return

        start_index = (current_page - 1) * 5
        keyboard = keyboard_to_show_tenders(listtender, page=current_page)
        selected_tender_index = start_index + 1  # Индекс первого тендера на текущей странице
        selected_tender = listtender[start_index] if start_index < len(listtender) else None
        if selected_tender:
            message_text = create_tender_message(selected_tender, selected_tender_index, len(listtender))
        else:
            message_text = "Нет доступных тендеров."

    # Проверка, нужно ли изменять сообщение и клавиатуру
    if callback_query.message.text != message_text or callback_query.message.reply_markup != keyboard:
        await bot.edit_message_text(message_text, callback_query.from_user.id, callback_query.message.message_id, reply_markup=keyboard)
    else:
        # Если сообщение и клавиатура не изменились, отправляем пустой ответ на callback_query
        await bot.answer_callback_query(callback_query.id)




#
#
# def create_tender_message(tender_data, tender_number, total_tenders):
#     message = (
#         f"Тендер №{tender_number} из {total_tenders}\n"
#         f"Объект закупки: {tender_data[3]}\n"
#         f"Регион закупки: {tender_data[12]}\n"
#         f"Начальная цена: {tender_data[4]}\n"
#         f"Заказчик: {tender_data[5]}\n"
#         f"Дата размещения: {tender_data[6]}\n"
#         f"Дата окончания: {tender_data[7]}\n"
#         f"Ссылка: {tender_data[2]}"
#     )
#     return message
#
# # Функция для создания инлайн-клавиатуры с кнопками тендеров и навигации
# def keyboard_to_show_tenders(listtender, selected_tender_index=None, page=1, page_size=5):
#     # Определяем диапазон тендеров для отображения на текущей странице
#     start_index = (page - 1) * page_size
#     end_index = start_index + page_size
#     current_tenders = listtender[start_index:end_index]
#
#     # Создаем список кнопок для текущих тендеров
#     buttons_tender = []
#     for index, tender in enumerate(current_tenders):
#         tender_number = start_index + index + 1
#         button_text = f'Тендер {tender_number}'
#         if selected_tender_index == tender_number:
#             button_text += ' ✅'
#         buttons_tender.append(types.InlineKeyboardButton(button_text, callback_data=f'tender_{tender_number}'))
#
#     # Создаем инлайн-клавиатуру с кнопками для текущих тендеров
#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     keyboard.add(*buttons_tender)
#
#     # Определяем количество страниц
#     total_pages = (len(listtender) + page_size - 1) // page_size
#
#     # Создаем кнопки для переключения страниц
#     navigation_buttons = []
#     if page > 1:
#         navigation_buttons.append(types.InlineKeyboardButton('⬅️', callback_data=f'prev_page_tenders_{page - 1}'))
#     navigation_buttons.append(types.InlineKeyboardButton(f'{page}/{total_pages}', callback_data='current_page'))
#     if page < total_pages:
#         navigation_buttons.append(types.InlineKeyboardButton('➡️', callback_data=f'next_page_tenders_{page + 1}'))
#
#     # Добавляем кнопки навигации в клавиатуру
#     keyboard.row(*navigation_buttons)
#
#     return keyboard
#
#
#
#
#
#
# # from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
#
#
# #
# #
# #
# # def keyboard_to_show_tenders(listtender, selected_tender_index=None, page=1, page_size=5):
# #     # Определяем диапазон тендеров для отображения на текущей странице
# #     start_index = (page - 1) * page_size
# #     end_index = start_index + page_size
# #     current_tenders = listtender[start_index:end_index]
# #
# #     # Создаем список кнопок для текущих тендеров
# #     buttons = []
# #
# #     button_text = 'Тендер 1 ✅'
# #     for index, tender in enumerate(current_tenders):
# #
# #         tender_number = start_index + index + 1
# #         button_text = f'Тендер {tender_number}'
# #         print(button_text)
# #
# #     if selected_tender_index == tender_number:
# #         button_text += ' ✅'
# #
# #
# #
# #
# #
# #
# #
# #         buttons.append(InlineKeyboardButton(button_text, callback_data=f'tender_{tender_number}'))
# #
# #     # Создаем инлайн-клавиатуру с кнопками для текущих тендеров
# #     keyboard = InlineKeyboardMarkup(row_width=1)
# #     keyboard.add(*buttons)
# #
# #     # Определяем количество страниц
# #     total_pages = (len(listtender) + page_size - 1) // page_size
# #
# #     # Создаем кнопки для переключения страниц
# #     navigation_buttons = []
# #     if page > 1:
# #         navigation_buttons.append(InlineKeyboardButton('⬅️', callback_data=f'prev_page_{page - 1}'))
# #     navigation_buttons.append(InlineKeyboardButton(f'{page}/{total_pages}', callback_data='current_page'))
# #     if page < total_pages:
# #         navigation_buttons.append(InlineKeyboardButton('➡️', callback_data=f'next_page_{page + 1}'))
# #
# #     # Добавляем кнопки навигации в клавиатуру
# #     keyboard.row(*navigation_buttons)
# #
# #     return keyboard
# #
# # def create_tender_message(tender, tender_number, total_tenders):
# #
# #
# #     return f"Тендер №{tender_number} из {total_tenders} \nОбъект закупки: {tender[3]}\nРегион закупки: {tender[12]} \nНачальная цена: {tender[4]} \nЗаказчик: {tender[5]} \nДата размещения: {tender[6]}\nДата окончания: {tender[7]}\nСсылка: {tender[2]}"
# #
# #
# #
# #
# #
# #
# #
# #
# #
#
# # Пример использования функции в хэндлере
# # @dp.message_handler(commands=['show_tenders'])
# # async def show_tenders(message: types.Message):
# #     # Пример списка тендеров
# #     listtender = [
# #         (10, '0373200017324000297', 'https://zakupki.gov.ru/epz/order/notice/ea20/view/common-info.html?regNumber=0373200017324000297', 'Поставка маркированных конвертов с литерой А', '120000,00', 'ГОСУДАРСТВЕННОЕ КАЗЕННОЕ УЧРЕЖДЕНИЕ ГОРОДА МОСКВЫ "ДИРЕКЦИЯ ЗАКАЗЧИКА ЖИЛИЩНО-КОММУНАЛЬНОГО ХОЗЯЙСТВА И БЛАГОУСТРОЙСТВА СЕВЕРО-ЗАПАДНОГО АДМИНИСТРАТИВНОГО ОКРУГА"', '09.07.2024', '31 рабочих дней', '11.07.2024', 'РОСЭЛТОРГ (АО«ЕЭТП»)', 'Нету значения', 'Электронный аукцион', 'Москва', 'Подача заявок', 0),
# #         # Добавьте еще тендеры сюда
# #     ]
# #
# #     keyboard = keyboard_to_show_tenders(listtender)
# #     message_text = create_tender_message(listtender[0], 1, len(listtender))
# #     await message.answer(message_text, reply_markup=keyboard)
