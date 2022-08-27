from aiogram import types, Dispatcher
from config import dp, bot
from keyboard.client import kb_keyboard, service_key, serv_key, service_salon
from keyboard.client import master_salon, info_salon_info
from aiogram.dispatcher.filters import Text
from parsing.client import service, service_id, date_id, date_master, time_master, work_salon_info
from parsing.client import master_select, master_cat, master_serv_cat, master_serv_date, master_time_date
import sqlite3 as sq

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


base = sq.connect('nicole.db')
cur = base.cursor()


class FSMAuth(StatesGroup):
    id_client = State()
    phone = State()
    password = State()


@dp.message_handler(commands=['start'])
async def start_sent(message: types.Message):

    text = f'Здравствуйте. Наш бот  может записать вас на прием по номеру телефона и паролю.\n' \
           f'Если вы первый раз хотите записаться, перейдите по ссылке: \n' \
           f'https://hipolink.me/grooming_nicole\n' \
           f'Если не помните пароль перейдите на сайт: \n' \
           f'https://dikidi.ru/ для восстановления пароля.'

    await bot.send_message(message.from_user.id, text, reply_markup=kb_keyboard)
    await message.delete()


# Вывод салонов по кнопке услуги
@dp.message_handler(Text(equals="Услуги"))
async def salon_service(message: types.Message):

    text = "Выберите удобный для вас салон"

    await message.answer(text, reply_markup=service_salon(text))


# Вывод категорий по кнопке услуги
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('ID|'))
async def cat_service(call: types.CallbackQuery):

    salon = call.data.split('|')[1]
    mr = service(int(salon))

    await call.message.answer('Выберите категорию', reply_markup=service_key(mr))
    '''await call.message.delete()'''
    await call.answer()


# Вывод услуг по кнопке услуги
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('serv|'))
async def ser_callback_run(call: types.CallbackQuery):

    serv = call.data.split('|')[1]
    salon = call.data.split('|')[2]
    mr = service_id(int(salon), int(serv))

    if len(mr) < 50:
        await call.message.answer('Выберите услугу', reply_markup=serv_key(mr))
        '''await call.message.delete()'''
        await call.answer()
    else:
        one = mr[0:50]
        two = mr[50:len(mr)+1]

        await call.message.answer('Выберите услугу', reply_markup=serv_key(one))
        await call.message.answer('Продолжение услуг', reply_markup=serv_key(two))
        '''await call.message.delete()'''
        await call.answer()


# Вывод доступных дат по кнопке услуги
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('usl|'))
async def date_callback_run(call: types.CallbackQuery):

    usl_id = call.data.split('|')[1]
    salon = call.data.split('|')[2]
    item = call.data.split('|')[3]
    mr = date_id(int(salon), int(usl_id))

    await call.message.answer('Выберите дату', reply_markup=service_key(mr))
    '''await call.message.delete()'''
    await call.answer()


# Вывод мастера по кнопке услуги
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('dat|'))
async def master_callback_run(call: types.CallbackQuery):

    date = call.data.split('|')[1]
    salon = call.data.split('|')[2]
    usluga = call.data.split('|')[3]
    mr = date_master(int(salon), date, int(usluga))

    await call.message.answer('Выберите мастера', reply_markup=service_key(mr))
    '''await call.message.delete()'''
    await call.answer()


# Вывод доступного времени по кнопке услуги
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('mast|'))
async def time_callback_run(call: types.CallbackQuery):

    date = call.data.split('|')[1]
    salon = call.data.split('|')[2]
    usluga = call.data.split('|')[3]
    master = call.data.split('|')[4]
    mr = time_master(int(salon), date, int(usluga), master)

    await call.message.answer('Выберите время', reply_markup=service_key(mr))
    '''await call.message.delete()'''
    await call.answer()


# Запрос на номер телефона по кнопке услуги


# Вывод салонов по кнопке специалисты
@dp.message_handler(Text(equals="Специалисты"))
async def salon_master(message: types.Message):
    text = "Выберите удобный для вас салон"
    await message.answer(text, reply_markup=master_salon(text))
    '''await message.delete()'''


# Вывод списка мастеров по кнопке специалисты
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('M_ID|'))
async def cat_master(call: types.CallbackQuery):

    salon = call.data.split('|')[1]
    mr = master_select(int(salon))

    await call.message.answer('Выберите мастера', reply_markup=service_key(mr))
    '''await call.message.delete()'''
    await call.answer()


# Вывод категорий по кнопке специалисты
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('MSal|'))
async def master_usluga(call: types.CallbackQuery):

    salon = call.data.split('|')[1]
    master = call.data.split('|')[2]
    mr = master_cat(int(salon), int(master))

    await call.message.answer('Выберите категорию', reply_markup=service_key(mr))
    '''await call.message.delete()'''
    await call.answer()


# Вывод услуг по кнопке специалисты
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('Mcat|'))
async def master_categories(call: types.CallbackQuery):

    salon = call.data.split('|')[1]
    master = call.data.split('|')[2]
    cat = call.data.split('|')[3]
    mk = master_serv_cat(int(salon), int(master), int(cat))

    if len(mk) < 45:
        await call.message.answer('Выберите услугу', reply_markup=serv_key(mk))
        '''await call.message.delete()'''
        await call.answer()
    else:
        one = mk[0:45]
        two = mk[45:len(mk) + 1]

        await call.message.answer('Выберите услугу', reply_markup=serv_key(one))
        await call.message.answer('Продолжение услуг', reply_markup=serv_key(two))
        '''await call.message.delete()'''
        await call.answer()


# Вывод даты по кнопке специалисты
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('MUC|'))
async def master_date_run(call: types.CallbackQuery):

    salon = call.data.split('|')[1]
    master = call.data.split('|')[2]
    usluga = call.data.split('|')[4]
    mr = master_serv_date(int(salon), int(master), int(usluga))
    pusto = []

    if mr == pusto:
        await call.message.answer(f'На выбранную вами услугу недостаточно\n'
                                  f'свободного времени или она недоступна\n'
                                  f'для онлайн-записи. Попробуйте позже или\n'
                                  f'обратитесь к специалисту по телефону.')
    else:
        await call.message.answer('Выберите дату', reply_markup=service_key(mr))
        '''await call.message.delete()'''
        await call.answer()


# Вывод времени по кнопке специалисты
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('MDC|'))
async def master_time_run(call: types.CallbackQuery):
    print('4')
    salon = call.data.split('|')[1]
    master = call.data.split('|')[2]
    usluga = call.data.split('|')[3]
    date = call.data.split('|')[4]
    mr = master_time_date(int(salon), int(master), int(usluga), date)

    await call.message.answer('В разработке', reply_markup=service_key(mr))
    '''await call.message.delete()'''
    await call.answer()


# Вывод списка салонов по кнопке информация
@dp.message_handler(Text(equals="Информация о салонах"))
async def info_salon(message: types.Message):
    text = "Выберите салон"
    await message.answer(text, reply_markup=info_salon_info(text))


# Вывод информации о салоне
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('ISw|'))
async def salon_info_salon(call: types.CallbackQuery):

    salon = call.data.split('|')[1]
    mr = work_salon_info(int(salon))

    await call.message.answer(mr)
    '''await call.message.delete()'''
    await call.answer()


@dp.message_handler(Text(equals="Помощь"))
async def info_bot(message: types.Message):
    text = f"Для записи в салон необходимо нажать на кнопку Услуги или Мастера.\n" \
           f"Для получения информации о салонах нажать на кнопку Информация о салонах.\n" \
           f"Если не отображаются кнопки снизу, необходимо написать /start.\n" \
           f"Для получения информации о работе бота нажать кнопку Помощь."
    await message.answer(text, reply_markup=kb_keyboard)
    '''await message.delete()'''


















# Регистрация команд
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_sent, commands=['start', 'help'])
    dp.register_message_handler(salon_service)
    dp.register_message_handler(cat_service)
    dp.register_message_handler(ser_callback_run)
    dp.register_message_handler(date_callback_run)
    dp.register_message_handler(master_callback_run)
    dp.register_message_handler(time_callback_run)

    dp.register_message_handler(salon_master)
    dp.register_message_handler(cat_master)

    dp.register_message_handler(info_salon)
    dp.register_message_handler(info_bot)

    dp.register_message_handler(salon_info_salon)

    dp.register_message_handler(master_usluga)

    dp.register_message_handler(master_categories)

    dp.register_message_handler(master_date_run)

    dp.register_message_handler(master_time_run)
