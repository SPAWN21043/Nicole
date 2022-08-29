import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv


load_dotenv()


storage = MemoryStorage()


TOKEN = os.getenv('S_TOKEN')
URL_APP = ''

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)
