from datetime import datetime
from email import message
from types import MemberDescriptorType
import config
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import os

TOKEN = os.getenv('TOKEN')

logging.basicConfig(level=logging.INFO)

# dictionary of data
SUBSCRIPTIONS_INFO = {
    'name': ['price', 'date', 'valid']
}

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
# turning on logging to prevent missing/overlooking messages
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    info_button = types.KeyboardButton("Subscriptions Info")
    add_button = types.KeyboardButton("Add a New Subscription")
    delete_button = types.KeyboardButton("Remove a Subscription")
    statistics_button = types.KeyboardButton("Get Monthly Statistics")
    markup.add(info_button, add_button, delete_button, statistics_button)
    await message.reply(f"Welcome, {message.from_user.first_name}! This is Subscription Manager Bot. How can I help you?", reply_markup=markup)


@dp.message_handler(commands=['help'])
async def handle_help(message: types.Message):
    await message.reply(f'This is Subscription Manager Bot that helps you with tracking your subscriptions!\n\nThe bot has 3 functions:\n1. <b>Subsciptions Info</b>. Sends the list of all of your subscriptions along with the price and the expiration date.\n2.', parse_mode='html')


@dp.message_handler(commands=['time'])
async def get_time(message: types.Message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    test_button = types.KeyboardButton("Current Time")
    markup.add(test_button)
    current_time = datetime.now()
    await message.answer(current_time.strftime("%H:%M:%S of %d %b, %Y"), parse_mode=None, reply_markup=markup)


@dp.message_handler(commands=['print'])
async def testing(message: types.Message):
    await message.answer(SUBSCRIPTIONS_INFO)


@dp.message_handler(content_types=['text'])
async def echo(message: types.Message):
    if message.text == 'Subscriptions Info':
        final_msg = ''
        for name in SUBSCRIPTIONS_INFO:
            final_msg += f'- {name}: {SUBSCRIPTIONS_INFO[name]}\n'
        await message.answer(final_msg)
    elif message.text == 'Add a New Subscription':
        inline_markup = types.InlineKeyboardMarkup(row_width=2)
        netflix_button = types.InlineKeyboardButton(
            'Netflix', callback_data='netflix')
        yandex_plus_button = types.InlineKeyboardButton(
            'Yandex Plus', callback_data='yandex_plus')
        spotify_button = types.InlineKeyboardButton(
            'Spotify', callback_data='spotify')
        custom_button = types.InlineKeyboardButton(
            'Other', callback_data='custom')
        inline_markup.add(netflix_button, yandex_plus_button,
                          spotify_button, custom_button)
        await message.answer("What would you like to add?", reply_markup=inline_markup)
    elif message.text == 'Get Monthly Statistics':
        total = 0
        for name in SUBSCRIPTIONS_INFO:
            if SUBSCRIPTIONS_INFO[name][0].isdigit():
                total += SUBSCRIPTIONS_INFO[name][0]
        await message.answer(f"You spend {total}$ each month on subscriptions")
    else:
        await message.answer("I don't understand...")


# gets callback data as parameters
@dp.callback_query_handler(text=['netflix', 'yandex_plus', 'spotify', 'custom'])
async def handle_inline_callback(call: types.CallbackQuery):
    try:
        if call.message:
            if call.data == 'netflix':
                SUBSCRIPTIONS_INFO['netflix'] = [11.99, '12-05-2022', 1]
                await call.message.answer('Adding Netflix subscription')
            elif call.data == 'yandex_plus':
                SUBSCRIPTIONS_INFO['yandex_plus'] = [850, '24-11-2022', 3]
                await call.message.answer('Adding Yandex Plus subscription')
            elif call.data == 'spotify':
                SUBSCRIPTIONS_INFO['spotify'] = [2.99, '09-02-2022', 12]
                await call.message.answer('Adding Spotify subscription')
            elif call.data == 'custom':
                SUBSCRIPTIONS_INFO['custom'] = [0, '00-00-0000', 0]
                await call.message.answer('Adding Custom subscription')
    except Exception as e:
        print(repr(e))


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)
