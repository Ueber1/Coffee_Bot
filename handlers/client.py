from aiogram import types, Dispatcher
import create_bot
from create_bot import dp, bot
from keyboards.client_kb import kb_client
from data_base import sqlite_db
from aiogram.types.input_file import  InputFile
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from data_base.sqlite_db import sql_get_list
#from create_bot import id_consumer
'''КЛИЕНТСКАЯ ЧАСТЬ'''



Order = ''


class FSMClient(StatesGroup):
    supplements = State()
    description = State()
    bakery = State()
    final = State()

class FSMIKnow(StatesGroup):
    iknow = State()

async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Здравствуйте, это Coffeе Fjord бот!\n Сделайте заказ сразу или выберете что-то из меню', reply_markup=kb_client)


async def i_know(message: types.Message):
    await bot.send_message(message.from_user.id, "Напишите ваш заказ")
    await FSMIKnow.iknow.set()

async def send_order(message,state: FSMContext):
    #await sqlite_db.sql_read(message)
    global Order
    create_bot.id_consumer = message.from_user.id
    Order += message.text
    await bot.send_message(message.from_user.id, "Ваш заказ отправлен, пожалуйста, дождитесь ответа баристы")
    _list = list()
    await sql_get_list(_list)
    for x in _list:
        try:
            await bot.send_message(x, Order)
        except:
            print("Бот не смог написать баристе")
    await state.finish()

async def send_order_i_know(message,state: FSMContext):
    #await sqlite_db.sql_read(message)
    global Order
    Order = ''
    create_bot.id_consumer = message.from_user.id
    Order += message.text
    await bot.send_message(message.from_user.id, "Ваш заказ отправлен, пожалуйста, дождитесь ответа баристы")
    _list = list()
    await sql_get_list(_list)
    for x in _list:
        try:
            await bot.send_message(x, Order)
        except:
            print("Бот не смог написать баристе")
    await state.finish()


async def pizza_menu_command(message):
    global Order
    Order = ""
    photo1 = InputFile("Photos/1.jpg")
    photo2 = InputFile("Photos/2.PNG")
    await bot.send_photo(message.from_user.id, photo=photo1)
    await bot.send_photo(message.from_user.id, photo=photo2)
    await bot.send_message(message.from_user.id, "Напишите сюда, что из пункта меню вы выбрали")
    await FSMClient.supplements.set()

async def supplements(message):
    global Order
    Order += message.text
    await FSMClient.bakery.set()
    await bot.send_message(message.from_user.id, "Напишите сюда, что из добавок вы выбрали")


async def bakery(message):
    global Order
    Order += message.text
    photo3 = InputFile("Photos/3.jpg")
    await bot.send_photo(message.from_user.id, photo=photo3)
    await FSMClient.final.set()
    await bot.send_message(message.from_user.id, "Напишите сюда, что из выпечки вы выбрали")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_menu_command, text ='Меню')
    dp.register_message_handler(i_know, text ='Знаю')
    dp.register_message_handler(supplements, state=FSMClient.supplements)
    dp.register_message_handler(bakery, state=FSMClient.bakery)
    dp.register_message_handler(send_order, state=FSMClient.final)
    dp.register_message_handler(send_order_i_know, state=FSMIKnow.iknow)
