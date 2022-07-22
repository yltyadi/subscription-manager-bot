from turtle import st
from aiogram import Dispatcher, types

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from db import Database
import ast

db = Database("sqlite_db.db")


class RemoveSub(StatesGroup):
    waiting_for_index = State()
    waiting_for_confirmation = State()


async def remove(message: types.Message):
    # array of tuples in the form (id, user_id, 'dict of info')
    result_arr = db.get_info(message.from_user.id)
    if len(result_arr) == 0:
        await message.answer("No subscription to remove!")
        return
    final_msg = ""
    if len(result_arr) == 0:
        final_msg += "No subscriptions were recorded..."
    else:
        for i in range(len(result_arr)):
            # converting string to dictionary
            info_dict = ast.literal_eval(result_arr[i][2])
            final_msg += f"{str(i + 1)}. {info_dict['sub_name']}   {info_dict['sub_price']}$   {info_dict['sub_date']}   {info_dict['sub_duration']} months\n"

    await message.answer(f"Which one do want to remove from the the list? Write the number only!\n\n{final_msg}")
    await RemoveSub.waiting_for_index.set()


async def index_chosen(message: types.Message, state: FSMContext):
    if message.text[0] == '/':
        await message.answer("Finish removing the subscription")
        return
    if not message.text.lower().isdigit():
        await message.answer("Write digits only!")
        return
    result_arr = db.get_info(message.from_user.id)
    # checking that the number is inside the range
    if int(message.text) not in range(1, len(result_arr) + 1):
        await message.answer("Choose the number inside the list!")
        return

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add("Yes", "No")

    await state.update_data(sub_id=int(message.text) - 1)
    await RemoveSub.next()
    await message.answer("Do you want to remove this subscription? Yes/No", reply_markup=keyboard)


async def confirmation(message: types.Message, state: FSMContext):
    if message.text[0] == '/':
        await message.answer("Finish removing the subscription")
        return
    if message.text.lower() == 'yes':
        user_data = await state.get_data()
        index = user_data['sub_id']
        all_info = db.get_info(message.from_user.id)
        row_id = all_info[index][0]
        db.remove_subs(message.from_user.id, row_id)
        await message.answer("Successfully removed from the list!", reply_markup=types.ReplyKeyboardRemove())
        await state.reset_state(with_data=False)
    elif message.text.lower() == 'no':
        await message.answer("Removing process was cancelled!", reply_markup=types.ReplyKeyboardRemove())
        await state.reset_state(with_data=False)
    else:
        await message.answer("Write 'Yes' or 'No' only!")
        return


def register_handler_remove(dp: Dispatcher):
    dp.register_message_handler(remove, commands=['remove_sub'], state="*")
    dp.register_message_handler(
        index_chosen, state=RemoveSub.waiting_for_index)
    dp.register_message_handler(
        confirmation, state=RemoveSub.waiting_for_confirmation)
