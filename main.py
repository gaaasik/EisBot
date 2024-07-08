from aiogram.utils import executor
from bot.config_bot.config_bot import API_TOKEN
from bot.database.database import init_db
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram import executor
from bot.start_bot import dp
import bot.all_handlers.text_handlers

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)