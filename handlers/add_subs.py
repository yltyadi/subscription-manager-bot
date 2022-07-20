from ast import Add
from curses.ascii import isdigit
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from db import Database

available_subscriptions = ['Netflix 📺', 'Yandex Plus 🎁', 'Spotify 🎧', 'Custom']
db = Database('sqlite_db.db')


class AddSub(StatesGroup):
    waiting_for_name = State()
    waiting_for_price = State()
    waiting_for_date = State()
    waiting_for_duration = State()


# selecting subscriptions using keyboard and waiting until user chooses one
async def sub(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for name in available_subscriptions:
        keyboard.add(name)
    await message.answer("Select which subscription you want to add:", reply_markup=keyboard)
    await AddSub.waiting_for_name.set()


# handling the chosen subscription (ready or custom) then asking for price
async def sub_chosen(message: types.Message, state: FSMContext):
    if message.text[0] == '/':
        await message.answer("Finish adding the subscription")
        return
    if message.text not in available_subscriptions:
        await message.answer("Choose from the reply keyboard!")
        return
    if message.text.lower() == 'custom':
        await message.answer("Write what custom subscription you want to add: ")
        return
    await state.update_data(sub_name=message.text.lower())
    await AddSub.next()
    await message.answer("What is the price of the subscription?", reply_markup=types.ReplyKeyboardRemove())


# handling written price and asking for date
async def price_written(message: types.Message, state: FSMContext):
    if message.text[0] == '/':
        await message.answer("Finish adding the subscription")
        return
    if not message.text.lower().isdigit():
        await message.answer("Write digits only!")
        return
    await state.update_data(sub_price=message.text)
    await AddSub.next()
    await message.answer("What is the date you activated the subscription")


# handling written date and check if it is valid, then asking for duration
async def date_written(message: types.Message, state: FSMContext):
    if message.text[0] == '/':
        await message.answer("Finish adding the subscription")
        return
    if False:  # have to check if the written value is a valid date
        pass
    await state.update_data(sub_date=message.text)
    await AddSub.next()
    await message.answer("What is the duration of the subscription? If 1 month just type the number 1.")


# handling duration of the subscription and exiting the state
async def duration_written(message: types.Message, state: FSMContext):
    if message.text[0] == '/':
        await message.answer("Finish adding the subscription")
        return
    if not message.text.isdigit():
        await message.answer("Write digits only!")
        return
    await state.update_data(sub_duration=message.text)
    user_data = await state.get_data()
    result = str(user_data)
    db.add_subs(message.from_user.id, result)
    await message.answer(f"Your subsription <b>{user_data['sub_name']}</b> with a price of {user_data['sub_price']}$ purchased in {user_data['sub_date']} for {user_data['sub_duration']} months was successfully added!", parse_mode='html')
    await state.reset_state(with_data=False)


async def test(message: types.Message):
    if db.user_exists(message.from_user.id):
        pass
    else:
        db.add_subs(message.from_user.id, "99, 99-99-9999, 9")
        await message.answer(f"{message.from_user.id} is added to the DB")


async def print_test(message: types.Message):
    result = db.user_exists(message.from_user.id)
    await message.answer(result)
    if result:
        await message.answer(f"user {message.from_user.id} is in the DB")
    else:
        await message.answer(f"user {message.from_user.id} is NOT in the DB!!!")


# async def info(message: types.Message, state: FSMContext):
#     # user_data = await state.get_data()
#     # await message.answer(f"Subscriptions Information:\n{user_data}")
#     await message.answer(asyncio.gather(MemoryStorage().get_data(chat="458575002")))


def register_handler_add(dp: Dispatcher):
    dp.register_message_handler(sub, commands=['add_sub'], state="*")
    dp.register_message_handler(sub_chosen, state=AddSub.waiting_for_name)
    dp.register_message_handler(price_written, state=AddSub.waiting_for_price)
    dp.register_message_handler(date_written, state=AddSub.waiting_for_date)
    dp.register_message_handler(
        duration_written, state=AddSub.waiting_for_duration)
    # dp.register_message_handler(
    #     info, commands=['info_sub'], state="*")
    dp.register_message_handler(test, commands=['test'])
    dp.register_message_handler(print_test, commands=['print_test'])
