from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp
from aiogram.dispatcher.filters import Text
from data_base.sqlite_db import sql_add_command
from keyboards import admin_kb
from create_bot import bot


ID = 901272435
"""Проверка в каждом хендлере нужна т.к. бот не понимает кто ему пишет, он просто переходит в другое состаяние"""


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


#Начало диалога загрузки нового пункта меню
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await bot.send_message(message.from_user.id, 'Hello, mr Admin!', reply_markup=admin_kb.button_case_admin)
        await FSMAdmin.photo.set()
        await message.reply('Load a photo')
#Catch a first answer from user and write it in dict


async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
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
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await sql_add_command(state)
        await state.finish()
        await message.reply('OK')
def register_handlers_admin(dp:Dispatcher):
    dp.register_message_handler(cm_start, commands=['Load'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands='отмена')
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
