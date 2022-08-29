from aiogram import types, Dispatcher
from config import dp, bot


@dp.message_handler()
async def other_commands(message: types.Message):
    await bot.send_message(message.from_user.id, "Такой команды нет")


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(other_commands)
