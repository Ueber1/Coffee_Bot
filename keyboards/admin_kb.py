from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
#Кнопки клавиатуры админа
button_list = KeyboardButton('Список барист')
button_add = KeyboardButton('Добавить баристу')
button_delete = KeyboardButton('Удалить баристу')
button_exit = KeyboardButton('Отмена')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(button_list)\
                    .add(button_add).add(button_delete).add(button_exit)