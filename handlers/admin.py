

"""===================================ADMIN PART==================================="""


from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from create_bot import bot, dp
from data_base import sqldb
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from keyboards import admin_kb
from keyboards import client_kb


ID = None


class FSMAdmin(StatesGroup):
    name = State()
    age = State()
    contact = State()
    information = State()
    photo = State()

#Проверка на модера
async def make_changes_command(msg : types.Message):
    global ID
    ID = msg.from_user.id
    await bot.send_message(msg.from_user.id, 'Что надо хозяин??', reply_markup=admin_kb.kb)
    await msg.delete()

#Список имен
async def list_of_names(msg : types.Message):
    await sqldb.sql_read(ID)

#Начало диолога
async def fsm_start(msg : types.Message):
    await FSMAdmin.name.set()
    await msg.reply(f"Как тебя зовут?", reply_markup=client_kb.client_kb2)

#Выход из состояния
async def cancel_fsm(msg : types.Message, state : FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await msg.reply(f"Оки", reply_markup=client_kb.client_kb1)

#Первый ответ
async def load_name(msg : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['name'] = msg.text
    await FSMAdmin.next()
    await msg.reply("Сколько тебе лет?")

#Второй ответ
async def load_age(msg : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['age'] = msg.text
    await FSMAdmin.next()
    await msg.reply('Как можно с вами связаться?')

#Третий ответ
async def load_contact(msg : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['contact'] = msg.text
    await FSMAdmin.next()
    await msg.reply('Расскажи о себе')

#Четвертый ответ
async def load_information(msg : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['information'] = msg.text
    await FSMAdmin.next()
    await msg.reply('Пришлите ваше фото, пожалуйста')

async def load_photo(msg : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['photo'] = msg.photo[-1].file_id
    try:
        await sqldb.insert_data_command(state)
        print("New data was added to database")
        try:
            await bot.send_message(chat_id=ID, text=f"Босс у вас новый клиент")
            await sqldb.sql_read(ID)
        except:
            await bot.send_message(msg.from_user.id, f"Данные успешно заполнены, подождите пока с вами не свяжутся",
                                       reply_markup=client_kb.client_kb1)
    except:
        await bot.send_message(msg.from_user.id, f"Произошла ошибка добавления в базу данных",
                                reply_markup=client_kb.client_kb1)

    await state.finish()

#Удаление предмета1
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query : types.CallbackQuery):
    await sqldb.sql_delete_command(callback_query.data.replace("del ", ""))
    await callback_query.answer(text=f"{callback_query.data.replace('del ', '')} удалена", show_alert=True)

#Удаление предмета2
async def delete_item(message : types.Message):
    if message.from_user.id == ID:
        read = await sqldb.sql_read2()
        for ret in read:
            await bot.send_photo(ID, ret[-1], f'Имя: {ret[0]}\nВозраст: {ret[1]}\nКонтакт: {ret[2]}\nИнформация: {ret[3]}', reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton(f"Удалить {ret[0]}", callback_data=f"del {ret[0]}")))
#Выход из админки
async def leave_admin(msg : types.Message):
    if msg.from_user.id == ID:
        await msg.reply('Вы вышли из админ-меню', reply_markup=client_kb.client_kb1)

def register_admin_handlers(dp : Dispatcher):
    dp.register_message_handler(fsm_start, commands=['Записаться'], state=None)
    dp.register_message_handler(cancel_fsm, state='*', commands=['Отмена'])
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_age, state=FSMAdmin.age)
    dp.register_message_handler(load_contact, state=FSMAdmin.contact)
    dp.register_message_handler(load_information, state=FSMAdmin.information)
    dp.register_message_handler(load_photo,content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(make_changes_command, commands=['moder'], is_chat_admin=True)
    dp.register_message_handler(list_of_names, commands=['Список'])
    dp.register_message_handler(delete_item, commands=['Удалить'])
    dp.register_message_handler(leave_admin, commands=['Выход'])