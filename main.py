from aiogram import types
from aiogram.utils import executor
from data_base import sqldb
from create_bot import bot, dp

async def on_start_bot(_):
    print('Bot is online now')
    sqldb.sql_start()

from handlers import admin, client
client.register_message_handler(dp)
admin.register_admin_handlers(dp)




executor.start_polling(dp, skip_updates=True, on_startup=on_start_bot)