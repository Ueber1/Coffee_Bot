# -*- coding: utf-8 -*-
import string
import json
from aiogram import types, Dispatcher
from create_bot import dp, bot, id_consumer
import create_bot

ides = {'id_valera': 562051066, 'id_lera': 1164486775, 'id_anfisa': 755065667, 'id_nikita': 634495823, 'id_vanya': 1121483319}
'''Common part'''
#@dp.message_handler()
async def echo_send(message: types.Message):
    for id in ides.values():
        if message.from_user.id == id:
            try:
                await bot.send_message(create_bot.id_consumer, "Ответ баристы: "+message.text)
            except:
                print("valera пишет тому, кому нельзя")



"""async def echo_send(message: types.Message):
    if {i.lower().translate(str.maketrans('','',string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply('Маты запрещены')
        await message.delete()
    else:
        #await message.answer(message.text)
        #await message.reply(message.text)
        await bot.send_message(id_valera, message.text)
"""
def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)

