# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# coding: utf8

from python.config import *
from python.parsing import *
import re

#from db import * если будем использовать базу данных

from telebot import types # для указание типов
import telebot

bot = telebot.TeleBot(TOKEN)

savedFltr = types.InlineKeyboardButton("Сохранёные поиски 💾 ", callback_data='createFltrSrch')
configNtfc = types.InlineKeyboardButton("Настройки уведомлений", callback_data='configNtfc')
returnToMain = types.InlineKeyboardButton("Вернуться в меню 📃", callback_data='returnToMain')
returnBack = types.InlineKeyboardButton("Назад 🔙", callback_data='returnBack')
#savedFltr = types.InlineKeyboardButton("Сохранёные поиски 💾 ", callback_data='createFltrSrch')


# Словарь соответствия ме жду текстом сообщения и знаками зодиака


@bot.message_handler(commands=['start'])
def send_welcome(message):
    add_user_to_db(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markupAllow = types.InlineKeyboardMarkup()
    markupInline = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton("🔍 Поиск тендеров")
    btn2 = types.KeyboardButton("🚀Больше возможностей")
    btn3 = types.KeyboardButton("👨‍💻 Обратная связь")
    btn4 = types.KeyboardButton("📚 Помощь")

    button1 = types.InlineKeyboardButton("Начать поиск ✅", callback_data='startfinder', message=message)
    configNtfc = types.InlineKeyboardButton("Настройки уведомлений", callback_data='configNtfc')
    button2 = types.InlineKeyboardButton("Вернуться в меню", callback_data='returntomain')
    markupAllow.add(button1, button2)
    markup.add( btn3,btn1,btn2, btn4)
    createFltrSrch = types.InlineKeyboardButton("Создание фильтра поиска 🔍 ", callback_data='createFltrSrch')
    markupInline.add(createFltrSrch,savedFltr,configNtfc)


    bot.send_message(message.chat.id, text="Привет! Я тестовый бот для поиска тендеров, скоро здесь появится инструкция для использования", reply_markup=markup)

    bot.send_message(message.from_user.id, text="Выбери нужное меню для поиска:",reply_markup=markupInline)

@bot.message_handler(commands=['🔍 Поиск тендеров'])



@bot.message_handler(content_types=['text'])
def func(message):

    markupReturntoMain = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Вернуться на главную страницу", callback_data='return')
    markupReturntoMain.add(button1)


    if (message.text == "🔍 Поиск тендеров"):
        #bot.register_next_step_handler(message, outputList)
        print()
    elif (message.text == "❓ Задать вопрос"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("🚀Больше возможностей")
        btn2 = types.KeyboardButton("📚 Помощь")
        back = types.KeyboardButton("👨‍💻 Обратная связь")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup,)

    elif (message.text == "📚 Помощь"):
        bot.send_message(message.chat.id, "📚 Помощь \n \n Наш сейчас находится на стадии тестирования и предоставляет собой удобный сервис для автоматического отслеживания за появлением новых тендеров на площадке zakupki.gov.ru. "
                                          "\n \n Чтобы начать пользоваться ботом, нажмите на кнопку «🔍 Поиск тендеров», введите ключевое слово, по которому будет проводиться поиск тендеров, "
                                          "и выберите регион(ы) тендеров. \n \n Не забудьте нажать кнопку Закончить выбор- для подтверждения своего выбора. \n\n  Чтобы удалить ключевое слово, нажмите "
                                          "на кнопку 📈 Мои тендеры, затем выберите ключевое слово для удаления и нажмите кнопку ❌Удалить.\n \n 👨‍💻 По всем вопросам обращайтесь к @gaaasik")
    elif message.text == "👨‍💻 Обратная связь":
        bot.send_message(message.chat.id, text="👨‍💻 Обратная связь\n  \n Если у вас есть вопросы, предложения или вы хотите сообщить об ошибке, то вы можете обратиться к нашему техническому специалисту \n \n  👨‍💻 По всем вопросам обращайтесь к @gaaasik ")
    elif message.text == "🚀Больше возможностей":
        bot.send_message(message.chat.id,text="🚀Больше возможностей \n \n Расширение функционала - это платная подписка, которая позволяет в полной мере использовать наш сервис.\n \n "
                              "Функционал:\n — Получения выгрузки тендеров в Excel файле\n — Просмотр истории найденных тендеров\n — Подписка на избранные тендеры \n \n"
                              "В дальнейшем функционал будет дополняться!\n \nСтоимость расширения функционала — писят рублей")

    elif (message.text == "Вернуться в главное меню"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Поздороваться")
        button2 = types.KeyboardButton("Задать вопрос")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, text="На такую комманду я не запрограммирован, выберите нужное меню")

def create(message):
    bot.send_message(message.chat.id, "Подтвердите поиск")
    markupAllow = types.InlineKeyboardMarkup()

    finderCallback_str = str('startfinder') + '|' + message.text

    # markupAllow.add(createFltrSrch)
    # markupAllow.add(savedFltr)
    # markupAllow.add(configNtfc)
    # markupAllow.add(returnToMain)

    bot.send_message(message.chat.id, text="Начать поиск тендеров с ключевым словом: \n \n"+message.text+" ? \n \n нажмите Да или Нет", reply_markup=markupAllow)

    print("Сообщение")
    #print(message)
    #print(parseEis(message))

def check_answers(msg):
    print('start check ansewr')
    notFound ="Ничего не найдено"
    errorWithBot = "Ошибка запроса"
    tenders = parseEis(msg)

    try:
        if len(tenders) == 0:
            return notFound
        else:
            return tenders
    except:
        print("Something went wrong")
        return errorWithBot


# def check_answers(message):
#     #print(message.text)
#     if message.text == "Начать поиск ✅":
#         try:
#             tenders = parseEis(msg)
#             print("что то тут есть")
#             if tenders == 0:
#                 bot.send_message(message.chat.id, text="Ошибка парсера")
#             else:
#                 chat_id = message.chat.id
#                 print('\n'.join(map(str, tenders)))
#                 bot.send_message(chat_id, '\n'.join(map(str, tenders)))
#         except:
#             bot.send_message(message.chat.id, text="Ошибка")

@bot.callback_query_handler(func=lambda call: re.search('createFltrSrch', call.data))  # Ловим коллбэк от кнопки. Нам передается объект CallbackQuery который содержит поле data и message. Сейчас нам нужно из даты достать наше слово которое мы передали в атрибуте callback_data
def create_finder(callback_query: types.CallbackQuery):
    print(callback_query.data)
    markupMenuCreateFltr = types.InlineKeyboardMarkup(row_width=1)
    inputKeyFind = types.InlineKeyboardButton("Ввести ключевое слово для поиска 🔍 ", callback_data='inputKeyFind')
    inputRegion = types.InlineKeyboardButton("Выберете регион 🗺️ ", callback_data='inputRegion')
    inputPrice = types.InlineKeyboardButton("Выберете цену ₽ ", callback_data='inputPrice')
    markupMenuCreateFltr.add(inputKeyFind,inputRegion,inputPrice)
    bot.send_message(callback_query.message.chat.id,text="Заполните данные фильтра",reply_markup=markupMenuCreateFltr)
    print("Зашли в кнопку квери")

@bot.callback_query_handler(func=lambda call: re.search('inputKeyFind', call.data))# Ловим коллбэк от кнопки. Нам передается объект CallbackQuery который содержит поле data и message. Сейчас нам нужно из даты достать наше слово которое мы передали в атрибуте callback_data
def create_finder(callback_query: types.CallbackQuery):
    print((callback_query.data))
    markupInputValueKey = types.InlineKeyboardMarkup(row_width=1)
    InputValueKey = types.InlineKeyboardButton("Введите наименование закупки", callback_data='InputValueKey')
    markupInputValueKey.add(InputValueKey)
    bot.send_message(callback_query.message.chat.id, text="Введите ключевое поле ", reply_markup=markupInputValueKey)

@bot.callback_query_handler(func=lambda call: re.search('InputValueKey', call.data))# Ловим коллбэк от кнопки. Нам передается объект CallbackQuery который содержит поле data и message. Сейчас нам нужно из даты достать наше слово которое мы передали в атрибуте callback_data
def create_finder(callback_query: types.CallbackQuery):
    #print(callback_query.message.text)
    inputkey = bot.send_message(callback_query.message.chat.id,'Введите ключевое слово')
    #bot.register_next_step_handler(inputkey, outputList)

@bot.callback_query_handler(func=lambda c: re.search('startfinder',c.data))#Ловим коллбэк от кнопки. Нам передается объект CallbackQuery который содержит поле data и message. Сейчас нам нужно из даты достать наше слово которое мы передали в атрибуте callback_data
def callback_answer(callback_query: types.CallbackQuery): #И отвечаем на него
    print("Тут надо запустить поиск")
    first_param = callback_query.data.split('|')[0]
    second_param = callback_query.data.split('|')[1]
    bot.answer_callback_query(
        callback_query.id,
        text='Мы начали поиск',
        show_alert=True
    )
    print(second_param,second_param)

    result = check_answers(second_param)
    print('htpekmfn ',result)
    if result == 0:
        bot.send_message(callback_query.message.chat.id, text="Тендеры не найдены")
    elif result == 2:
        bot.send_message(callback_query.message.chat.id,'Ощибка запроса')
    elif result == 1:
        bot.send_message(callback_query.message.chat.id, result)


#    print(data)





# Press the green button in the gutter to run the script.


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

bot.infinity_polling(interval=0)