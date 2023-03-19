

"""===================================CLIENT PART==================================="""


from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import client_kb
from aiogram.types import ReplyKeyboardRemove

async def start_command(msg : types.Message):
    await bot.send_message(msg.from_user.id, f"Привет {msg.from_user.first_name}.\nС моей помощью ты можешь записаться на занятие в IT CUBE", reply_markup=client_kb.client_kb1)
    await msg.delete()

def register_message_handler(dp : Dispatcher):
   dp.register_message_handler(start_command, commands=['start'])