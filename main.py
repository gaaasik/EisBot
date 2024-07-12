

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.config_bot.config_bot import API_TOKEN
from bot.database.database import init_db
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram import executor, contrib
from bot.start_bot import dp,bot
from bot.database.database import init_db
import bot.all_handlers.text_handlers
def notify_message():
    print("Бот запущен")
if __name__ == '__main__':
    #executor.start(dp, notify_message())
    init_db()
    executor.start_polling(dp, skip_updates=True)


# from aiogram import Bot, Dispatcher, types
#
# from bot.config_bot.config_bot import API_TOKEN
# from bot.database.database import init_db
# from bot.start_bot import dp, bot
# import bot.all_handlers.text_handlers
# def notify_message(dp):
#     print("Бот запущен")
#
# if __name__ == '__main__':
#     init_db()
#     dp.include_router(bot.all_handlers.text_handlers.my_router)
#     executor.start_polling(dp, skip_updates=True, on_startup=notify_message)