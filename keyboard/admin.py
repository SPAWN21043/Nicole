from aiogram.types import ReplyKeyboardMarkup


admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ['Все админы', 'Добавить админа']
admin_keyboard.add(*buttons)
buttons2 = ['Все салоны', 'Добавить салон']
admin_keyboard.add(*buttons2)
buttons3 = ['Вернуться']
admin_keyboard.add(*buttons3)
