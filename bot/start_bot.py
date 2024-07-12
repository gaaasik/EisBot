#
# #from aiogram import Router,F
# import logging
# from aiogram import Bot, Dispatcher
# from bot.config_bot.config_bot import API_TOKEN
# from bot.config_bot.config_bot import API_TOKEN
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import logging
from aiogram import Bot, Dispatcher
from bot.config_bot.config_bot import  API_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage


storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot,storage=storage)
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.INFO)

