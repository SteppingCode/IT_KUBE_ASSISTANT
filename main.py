from aiogram.utils import executor
from data_base import sqldb
from create_bot import dp
async def on_start_bot(_):
    print('Bot is online now')
    sqldb.sql_start()

from handlers import admin, client, other
client.register_message_handler(dp)
admin.register_admin_handlers(dp)
other.register_handlers_other(dp)




executor.start_polling(dp, skip_updates=True, on_startup=on_start_bot)
