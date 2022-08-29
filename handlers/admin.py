import os
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import dp, bot
from keyboard import clients, admin
from aiogram.dispatcher.filters import Text
from data_base import sql_db
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv


load_dotenv()


chief_admin = os.getenv('chief_admin')
master = os.getenv('master')


class FSMCreatAdmins(StatesGroup):
    id_admin = State()
    name = State()


class FSMCreateSalon(StatesGroup):
    title = State()
    adress = State()
    phone = State()
    id_vk = State()


@dp.message_handler(commands=['Administrator'])
async def start_admin(message: types.Message):

    user = message.from_user.id
    admin_admin = await sql_db.read_admin(user)

    if user == chief_admin or master or admin_admin:

        text = f'Вы находитесь в меню администратора.\n' \
               f'Для добавления администратора получите ID нового администратора.\n' \
               f'Чтобы новый администратор смог вам передать ID, ему необходимо в чате с ботом написать команду "/MyID".\n' \
               f'Для внесения его в базу нажмите кнопку Добавить админа.\n' \
               f'Чтобы удалить администратора нажмите кнопку Все админы и удалите нужного.\n' \
               f'Чтобы добавить салон нажмите кнопку добавить салон.\n' \
               f'Для добавления салона вам необходим ID салона, его можно посмотреть перейдя по ссылке:\n' \
               f'https://hipolink.me/grooming_nicole и посмотреть в адресной строке его номер.\n' \
               f'Чтобы удалить салон нажмите кнопку Все салоны и удалите нужный.'

        await bot.send_message(message.from_user.id, text, reply_markup=admin.admin_keyboard)
        await message.delete()

    else:
        await bot.send_message(message.from_user.id, "Нет такой команды", reply_markup=clients.kb_keyboard)
        await message.delete()


# Админ
@dp.message_handler(Text(equals="Добавить админа"), state=None)
async def creat_admin_admin(message: types.Message):
    user = message.from_user.id
    admin_admin = await sql_db.read_admin(user)

    if user == chief_admin or master or admin_admin:

        await bot.send_message(message.from_user.id, "Введите ID администратора")
        await FSMCreatAdmins.id_admin.set()

    else:

        await bot.send_message(message.from_user.id, "Нет такой команды", reply_markup=clients.kb_keyboard)
        await message.delete()


@dp.message_handler(state=FSMCreatAdmins.id_admin)
async def create_id_admin(message: types.Message, state: FSMContext):

    user = message.from_user.id
    admin_admin = await sql_db.read_admin(user)

    if user == chief_admin or master or admin_admin:

        async with state.proxy() as data:
            data['id_admin'] = int(message.text)
        await FSMCreatAdmins.next()
        await message.reply('Введите Имя')

    else:
        await state.finish()
        await bot.send_message(message.from_user.id, "Нет такой команды", reply_markup=clients.kb_keyboard)
        await message.delete()


# Ловим последний ответ и исполняем полученные данные
@dp.message_handler(state=FSMCreatAdmins.name)
async def create_name_admin(message: types.Message, state: FSMContext):

    user = message.from_user.id
    admin_admin = await sql_db.read_admin(user)

    if user == chief_admin or master or admin_admin:

        async with state.proxy() as data:
            data['name'] = message.text

        await sql_db.creat_admin(state)
        await state.finish()
        await message.reply("Администратор добавлен", reply_markup=admin.admin_keyboard)

    else:

        await state.finish()
        await bot.send_message(message.from_user.id, "Нет такой команды", reply_markup=clients.kb_keyboard)
        await message.delete()


@dp.message_handler(Text(equals="Все админы"))
async def delete_admin(message: types.Message):
    user = message.from_user.id
    admin_admin = await sql_db.read_admin(user)

    if user == chief_admin or master or admin_admin:

        read = await sql_db.read_all_admins()

        for ret in read:

            await bot.send_message(message.from_user.id, f'Администратор:\n'
                                                         f'Имя: {ret[1]}')
            await bot.send_message(
                message.from_user.id,
                text='⬆⬆⬆⬆⬆⬆⬆⬆',
                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                    f'Удалить {ret[1]}', callback_data=f'delAd|{ret[0]}'
                )
                )
            )

    else:

        await bot.send_message(message.from_user.id, "Нет такой команды", reply_markup=clients.kb_keyboard)
        await message.delete()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('delAd|'))
async def admin_delete_admin(call: types.CallbackQuery):

    admin_id = call.data.split('|')[1]
    await sql_db.delete_admin(int(admin_id))

    await call.message.answer('Администратор удален')
    '''await call.message.delete()'''
    await call.answer()


# Салон
@dp.message_handler(Text(equals="Добавить салон"), state=None)
async def creat_salon_admin(message: types.Message):
    user = message.from_user.id
    admin_admin = await sql_db.read_admin(user)

    if user == chief_admin or master or admin_admin:

        await bot.send_message(message.from_user.id, "Введите название салона")
        await FSMCreateSalon.title.set()

    else:

        await bot.send_message(message.from_user.id, "Нет такой команды", reply_markup=clients.kb_keyboard)
        await message.delete()


@dp.message_handler(state=FSMCreateSalon.title)
async def create_salon_name(message: types.Message, state: FSMContext):
    user = message.from_user.id
    admin_admin = await sql_db.read_admin(user)

    if user == chief_admin or master or admin_admin:

        async with state.proxy() as data:
            data['title'] = message.text
        await FSMCreateSalon.next()
        await message.reply('Введите адрес салона')

    else:
        await state.finish()
        await bot.send_message(message.from_user.id, "Нет такой команды", reply_markup=clients.kb_keyboard)
        await message.delete()


@dp.message_handler(state=FSMCreateSalon.adress)
async def create_ad_salon(message: types.Message, state: FSMContext):
    user = message.from_user.id
    admin_admin = await sql_db.read_admin(user)

    if user == chief_admin or master or admin_admin:

        async with state.proxy() as data:
            data['adress'] = message.text
        await FSMCreateSalon.next()
        await message.reply('Введите телефон салона')

    else:
        await state.finish()
        await bot.send_message(message.from_user.id, "Нет такой команды", reply_markup=clients.kb_keyboard)
        await message.delete()


@dp.message_handler(state=FSMCreateSalon.phone)
async def create_phone_salon(message: types.Message, state: FSMContext):
    user = message.from_user.id
    admin_admin = await sql_db.read_admin(user)

    if user == chief_admin or master or admin_admin:

        async with state.proxy() as data:
            data['phone'] = message.text
        await FSMCreateSalon.next()
        await message.reply('Введите ID салона')

    else:
        await state.finish()
        await bot.send_message(message.from_user.id, "Нет такой команды", reply_markup=clients.kb_keyboard)
        await message.delete()


# Ловим последний ответ и исполняем полученные данные
@dp.message_handler(state=FSMCreateSalon.id_vk)
async def create_id_salon(message: types.Message, state: FSMContext):
    user = message.from_user.id
    admin_admin = await sql_db.read_admin(user)

    if user == chief_admin or master or admin_admin:

        async with state.proxy() as data:
            data['id_vk'] = int(message.text)

        await sql_db.creat_salon(state)
        await state.finish()
        await message.reply("Салон добавлен", reply_markup=admin.admin_keyboard)

    else:

        await state.finish()
        await bot.send_message(message.from_user.id, "Нет такой команды", reply_markup=clients.kb_keyboard)
        await message.delete()


@dp.message_handler(Text(equals="Все салоны"))
async def delete_salon(message: types.Message):
    user = message.from_user.id
    admin_admin = await sql_db.read_admin(user)

    if user == chief_admin or master or admin_admin:
        read = await sql_db.read_all_salon()
        for ret in read:
            await bot.send_message(message.from_user.id, f'Салон:\n'
                                                         f'Имя: {ret[0]}\n'
                                                         f'Адрес: {ret[1]}')
            await bot.send_message(
                message.from_user.id,
                text='⬆⬆⬆⬆⬆⬆⬆⬆',
                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(
                    f'Удалить {ret[0]}', callback_data=f'delSa|{ret[3]}'
                )
                )
            )

    else:

        await bot.send_message(message.from_user.id, "Нет такой команды", reply_markup=clients.kb_keyboard)
        await message.delete()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('delSa|'))
async def salon_delete_salon(call: types.CallbackQuery):

    admin_id = call.data.split('|')[1]
    await sql_db.delete_salon_s(int(admin_id))

    await call.message.answer('Салон удален')
    '''await call.message.delete()'''
    await call.answer()


@dp.message_handler(Text(equals="Вернуться"))
async def back_return(message: types.Message):

    await message.answer('Вы в чате с ботом', reply_markup=clients.kb_keyboard)


# Регистрация команд
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(start_admin, commands=['Administrator'])

    dp.register_message_handler(creat_admin_admin, state=None)
    dp.register_message_handler(create_id_admin, state=FSMCreatAdmins.id_admin)
    dp.register_message_handler(create_name_admin, state=FSMCreatAdmins.name)
    dp.register_message_handler(delete_admin)
    dp.register_message_handler(admin_delete_admin)

    dp.register_message_handler(creat_salon_admin, state=None)
    dp.register_message_handler(create_salon_name, state=FSMCreateSalon.title)
    dp.register_message_handler(create_ad_salon, state=FSMCreateSalon.adress)
    dp.register_message_handler(create_phone_salon, state=FSMCreateSalon.phone)
    dp.register_message_handler(create_id_salon, state=FSMCreateSalon.id_vk)
    dp.register_message_handler(delete_salon)
    dp.register_message_handler(salon_delete_salon)

    dp.register_message_handler(back_return)

