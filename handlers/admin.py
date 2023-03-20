from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp
from aiogram.dispatcher.filters import Text
from data_base.sqlite_db import sql_add_command
from data_base.sqlite_db import sql_read
from data_base.sqlite_db import sql_del
from keyboards import admin_kb
from create_bot import bot


ID = [901272435,562051066]
"""Проверка в каждом хендлере нужна т.к. бот не понимает кто ему пишет, он просто переходит в другое состаяние"""


class FSMAdmin(StatesGroup):
    worker_editor = State()
    add_state = State()
    del_state = State()
    """names_list = State()"""
    '''description = State()'''
    '''price = State()'''


#Начало диалога загрузки нового пункта меню
async def cm_start(message: types.Message):
    if message.from_user.id == ID[0] or message.from_user.id == ID[1]:
        await bot.send_message(message.from_user.id, 'Hello, mr Admin! Say "отмена" for exit', reply_markup=admin_kb.button_case_admin)
        await FSMAdmin.worker_editor.set()
        """await message.reply('Load a photo')"""
    else:
        await bot.send_message(message.from_user.id, 'Sorry, you are not the Admin!')
#Catch a first answer from user and write it in dict
async def cm_list_wrks(message: types.Message):
    await sql_read(message)

async def cm_add_btn(message: types.Message,state: FSMContext):
    await message.reply('Пришлите имя - id')
    await FSMAdmin.add_state.set()
async def cm_add_wrk(message: types.Message,state: FSMContext):
    msg = message.text.split(' - ')
    async with state.proxy() as data:
        data['name'] = msg[0]
        data['id'] = msg[1]
    await message.reply(f'Ready:{msg[0]} = {msg[1]}')
    await sql_add_command(state)
    await state.finish()
    await FSMAdmin.worker_editor.set()
async def cm_del_btn(message: types.Message,state: FSMContext):
    await message.reply('Пришлите id')
    await FSMAdmin.del_state.set()
async def cm_del_wrk(message: types.Message,state: FSMContext):
    msg = message.text
    await sql_del(msg)
    await state.finish()
    await FSMAdmin.worker_editor.set()
    await message.reply('Ready')
async def load_photo(message: types.Message, state: FSMContext):
    await bot.reply(message.from_user.id, 'Sorry, you are not the Admin!')
    async with state.proxy() as data:
        data['name'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.reply('Now, write me a name')

#Catch the second answer
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Now, write me a description')

#Catch the third answer
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Now, write me a price')

#Catch the price
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = message.text
        await sql_add_command(state)
        await state.finish()
        await message.reply('OK')
        await state.finish()

#Выход из состояний
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')
def register_handlers_admin(dp:Dispatcher):
    dp.register_message_handler(cm_start, commands=['admin'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='Отмена', ignore_case=True), state="*")
    dp.register_message_handler(cm_list_wrks, state=FSMAdmin.worker_editor, text = "Список барист")
    dp.register_message_handler(cm_add_btn, state=FSMAdmin.worker_editor, text="Добавить баристу")
    dp.register_message_handler(cm_add_wrk, state=FSMAdmin.add_state)
    dp.register_message_handler(cm_del_btn, state=FSMAdmin.worker_editor, text="Удалить баристу")
    dp.register_message_handler(cm_del_wrk, state=FSMAdmin.del_state)
    """dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)"""
