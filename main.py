

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot.config_bot.config_bot import API_TOKEN
from bot.database.database import init_db
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram import executor, contrib
from bot.start_bot import dp,bot
from bot.database.database import init_db

from bot.all_handlers.create_search_filters import create_search, wait_keyword_from_user
from bot.all_handlers import showTendersInMessage, text_handlers
def notify_message():
    print("Бот запущен")
if __name__ == '__main__':
    #executor.start(dp, notify_message())
    init_db()
    executor.start_polling(dp, skip_updates=True)

