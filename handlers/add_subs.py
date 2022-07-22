from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
from datetime import datetime
from datetime import timedelta
import ast
from db import Database

available_subscriptions = ['Netflix 📺',
                           'Yandex Plus 🎁', 'Spotify 🎧', 'Custom 🖋', 'Cancel']
db = Database('sqlite_db.db')


class AddSub(StatesGroup):
    waiting_for_name = State()
    waiting_for_price = State()
    waiting_for_date = State()
    waiting_for_duration = State()


async def notification(message, user_data_map):
    # activation_date = datetime.now()
    # notify_date = activation_date + timedelta(minutes=2)
    activation_date = datetime.strptime(user_data_map['sub_date'], "%d-%m-%Y")
    months = user_data_map['sub_duration']
    name = user_data_map['sub_name']
    price = user_data_map['sub_price']
    # date after 30 days * months user indicated
    notify_date = activation_date + timedelta(days=30 * int(months))
    # sleeps only this function without stopping the entire code
    await asyncio.sleep((notify_date - activation_date).total_seconds())
    # await asyncio.sleep(30)
    await message.answer(f"Your <b>{name}</b> subscription is expiring today 😱.\n\n<u>It costs {price}$</u>. If you plan on cancelling it, do not forget to do so!", parse_mode="html")


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
        await message.answer("Finish adding the subscription.")
        return
    if message.text.lower() == 'cancel':
        await state.reset_state(with_data=False)
        await message.answer("The process was stopped.", reply_markup=types.ReplyKeyboardRemove())
        return
    if message.text == 'Custom 🖋':
        await message.answer("Write what custom subscription you want to add: ")
        return

    result_arr = db.get_info(message.from_user.id)
    for i in range(len(result_arr)):
        info_dict = ast.literal_eval(result_arr[i][2])
        if info_dict['sub_name'] == message.text.lower():
            await message.answer("The subscription already exists.")
            return

    await state.update_data(sub_name=message.text.lower())
    await AddSub.next()
    await message.answer("What is the price of the subscription?", reply_markup=types.ReplyKeyboardRemove())


# handling written price and asking for date
async def price_written(message: types.Message, state: FSMContext):
    if message.text[0] == '/':
        await message.answer("Finish adding the subscription")
        return

    isfloat = False
    try:
        float(message.text)
        isfloat = True
    except ValueError:
        await message.answer("Write digits only!")
        isfloat = False
        return

    await state.update_data(sub_price=message.text)
    await AddSub.next()
    await message.answer("What is the date you activated the subscription? Format is day-month-year")


# handling written date and check if it is valid, then asking for duration
async def date_written(message: types.Message, state: FSMContext):
    if message.text[0] == '/':
        await message.answer("Finish adding the subscription")
        return

    date_format = "%d-%m-%Y"
    isvalid = False
    try:
        isvalid = bool(datetime.strptime(message.text, date_format))
    except ValueError:
        isvalid = False

    if not isvalid:
        await message.answer("The date format is invalid!")
        return
    await state.update_data(sub_date=message.text)
    await AddSub.next()
    await message.answer("What is the duration of the subscription? If 1 month just type the number 1.")


# handling duration of the subscription and exiting the state
async def duration_written(message: types.Message, state: FSMContext):
    if message.text[0] == '/':
        await message.answer("Finish adding the subscription")
        return

    if not message.text.lower().isdigit():
        await message.answer("Write digits only!")
        return

    await state.update_data(sub_duration=message.text)
    user_data = await state.get_data()
    result = str(user_data)
    db.add_subs(message.from_user.id, result)
    await message.answer(f"Your subscription <b>{user_data['sub_name']}</b> with a price of {user_data['sub_price']}$ purchased in {user_data['sub_date']} for {user_data['sub_duration']} months was successfully added!", parse_mode='html')
    await state.reset_state(with_data=False)
    # sets notification parameters once the subscription is added
    await notification(message, user_data)


def register_handler_add(dp: Dispatcher):
    dp.register_message_handler(sub, commands=['add_sub'], state="*")
    dp.register_message_handler(sub_chosen, state=AddSub.waiting_for_name)
    dp.register_message_handler(price_written, state=AddSub.waiting_for_price)
    dp.register_message_handler(date_written, state=AddSub.waiting_for_date)
    dp.register_message_handler(
        duration_written, state=AddSub.waiting_for_duration)
