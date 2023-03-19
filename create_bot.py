from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = "6266524924:AAHztGiVhWAeUPdyqdiscxoiJIvpjmaM1Wc"

storage = MemoryStorage()

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
