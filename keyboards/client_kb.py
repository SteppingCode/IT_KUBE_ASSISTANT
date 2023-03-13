from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

client_btn1 = KeyboardButton('/Записаться')
client_btn2 = KeyboardButton('/Отмена')
client_kb1 = ReplyKeyboardMarkup(resize_keyboard=True)
client_kb1.row(client_btn1)
client_kb2 = ReplyKeyboardMarkup(resize_keyboard=True)
client_kb2.row(client_btn2)