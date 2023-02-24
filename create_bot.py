from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(token='6182715440:AAF0RgQqG8CNGwgtKHlw8KuRwLQCYfOsj2s')
dp = Dispatcher(bot, storage=storage)
id_consumer = 0