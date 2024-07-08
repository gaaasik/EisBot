from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from bot.config_bot.config_bot import API_TOKEN


#
# storage = MemoryStorage()
# bot = Bot(token=API_TOKEN)
# dp = Dispatcher(bot, storage=storage)
# dp.middleware.setup(LoggingMiddleware())
#
from aiogram import Bot, Dispatcher
from bot.config_bot.config_bot import API_TOKEN
storage = MemoryStorage()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot,storage=storage)

