from aiogram import Dispatcher, types


async def statistics(message: types.Message):
    await message.answer("Statistics")


def register_handler_statistics(dp: Dispatcher):
    dp.register_message_handler(statistics, commands=['statistics'])
