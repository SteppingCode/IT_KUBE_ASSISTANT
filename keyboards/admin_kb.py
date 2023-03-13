from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

delete_btn = KeyboardButton('/Удалить')
list_btn = KeyboardButton('/Список')
leave_btn = KeyboardButton('/Выход')

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.row(delete_btn, list_btn, leave_btn)