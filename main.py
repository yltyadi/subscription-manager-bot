from datetime import datetime
import config
import logging
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    await message.answer("Welcome!")


@dp.message_handler(commands=['time'])
async def get_time(message: types.Message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    test_button = types.KeyboardButton("Current Time")
    markup.add(test_button)
    current_time = datetime.now()
    await message.answer(current_time.strftime("%H:%M:%S of %d %b, %Y"))


@dp.message_handler(content_types=['text'])
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)


"""
from distutils.command.config import config
from email import message
import typing
import telebot
import config
from telebot import types
# import datetime

name = ''
price = 0
duration = 0
# date = datetime.datetime()


bot = telebot.TeleBot(config.TOKEN)  # starting the bot


@bot.message_handler(commands=['start'])
def welcome(message):
    # adding keyboard
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    info_button = types.KeyboardButton("Subscriptions Info")
    add_button = types.KeyboardButton("Add a New Subscription")
    statistics_button = types.KeyboardButton("Get Monthly Statistics")
    markup.add(info_button, add_button, statistics_button)

    # sending message / the reply keyboard sends message
    bot.send_message(message.chat.id, "Hello {0.first_name}! I am {1.first_name} Bot. How can I help you?".format(
        message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


# will handle any text message or command from reply keyboard
@bot.message_handler(content_types=['text'])
def handle_reply(message):
    if message.chat.type == 'private':
        if message.text == 'Subscriptions Info':
            bot.send_message(
                message.chat.id, "List of all subscriptions: \n1. Name Duration Price\n2. Name Duration Price\n3. Name Duration Price")
        elif message.text == 'Add a New Subscription':
            # creating inline buttons
            markup = types.InlineKeyboardMarkup(row_width=2)
            # callback data is the data taht is returned once the button is clicked
            netflix_button = types.InlineKeyboardButton(
                'Netflix', callback_data='netflix')
            yandex_plus_button = types.InlineKeyboardButton(
                'Yandex Plus', callback_data='yandex_plus')
            spotify_button = types.InlineKeyboardButton(
                'Spotify', callback_data='spotify')
            custom_button = types.InlineKeyboardButton(
                'Other', callback_data='custom')
            markup.add(netflix_button, yandex_plus_button,
                       spotify_button, custom_button)
            bot.send_message(
                message.chat.id, "What would you like to add?", reply_markup=markup)
        elif message.text == "Get Monthly Statistics":
            bot.reply_to(message, "Your monthly expenses: ")
        elif message.text.isdigit():  # only integers, not floats
            price = message.text
            bot.send_message(message.chat.id, price)
        else:
            bot.send_message(message.chat.id, "I don't understand...")


# handling inline keyboard replies
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'netflix':
                bot.send_message(call.message.chat.id, 'Adding Netlfix. Write')
                # bot.send_chat_action(call.message.chat.id, action=typing)
            elif call.data == 'yandex_plus':
                bot.send_message(call.message.chat.id, 'Adding Yandex Plus')
            elif call.data == 'spotify':
                bot.send_message(call.message.chat.id, 'Adding Spotify')
            elif call.data == 'custom':
                bot.send_message(call.message.chat.id,
                                 'Adding Custom Subscription')
            # remove inline buttons
            # bot.edit_message_text()
            # show alert
            # bot.answer_callback_query(
            #     chat_id=call.message.chat.id, show_alert=True, text="TESTING")
    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)
# bot.infinity_polling()
"""
