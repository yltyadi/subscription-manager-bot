from aiogram import Dispatcher, types


async def remove(message: types.Message):
    await message.answer("Removing")


def register_handler_remove(dp: Dispatcher):
    dp.register_message_handler(remove, commands=['remove_sub'])
