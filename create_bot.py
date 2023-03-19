from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

TOKEN = "6266524924:AAHztGiVhWAeUPdyqdiscxoiJIvpjmaM1Wc"

storage = MemoryStorage()
#PROXY_URL = "http://36.89.245.65:8080"
bot = Bot(token=TOKEN)#, proxy=PROXY_URL)
dp = Dispatcher(bot, storage=storage)

