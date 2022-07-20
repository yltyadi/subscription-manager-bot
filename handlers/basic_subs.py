from aiogram import Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime


async def start(message: types.Message):
    await message.reply(f"Welcome, {message.from_user.first_name}! This is Subscription Manager Bot. How can I help you?")


async def help(message: types.Message):
    await message.reply(f'This is Subscription Manager Bot that helps you with tracking your subscriptions and monthly expenses!\n\nThe bot has 3 main features:\n\n1. <b>Subsciptions Info</b>. Sends the list of all of your subscriptions along with the price and the expiration date.\n\n2. <b>Adding Subscriptions</b>. Adds subscription info to the database in the following form: name, price, activation date, duration. The same pattern applies to removing subscriptions.\n\n3. <b>Monthly Statistics</b>. Sends a monthly, financial analysis and statistics of all subscriptions. Helps to understand how much money we spend each month on various subscriptions.', parse_mode='html')


async def get_time(message: types.Message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    test_button = types.KeyboardButton("Current Time")
    markup.add(test_button)
    current_time = datetime.now()
    await message.answer(current_time.strftime("%H:%M:%S of %d %b, %Y"), parse_mode=None, reply_markup=markup)


def register_basic_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(help, commands=['help'])
    dp.register_message_handler(get_time, commands=['time'])
