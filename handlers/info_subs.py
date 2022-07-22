import ast
from calendar import month
from aiogram import Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import Database
import time

db = Database("sqlite_db.db")


async def info(message: types.Message):
    # array of tuples in the form (id, user_id, 'dict of info')
    result_arr = db.get_info(message.from_user.id)
    final_msg = ""
    if len(result_arr) == 0:
        final_msg += "No subscriptions were recorded..."
    else:
        for i in range(len(result_arr)):
            # converting string to dictionary
            info_dict = ast.literal_eval(result_arr[i][2])
            final_msg += f"{str(i + 1)}. {info_dict['sub_name']}   {info_dict['sub_price']}$   {info_dict['sub_date']}   {info_dict['sub_duration']} months\n"

    await message.answer(f"Subscriptions Information:\n\n{final_msg}")


async def statistics(message: types.Message):
    # array of tuples in the form (id, user_id, 'dict of info')
    result_arr = db.get_info(message.from_user.id)
    final_msg = ""
    total_price = 0
    if len(result_arr) == 0:
        final_msg += "No subscriptions were recorded..."
    else:
        for i in range(len(result_arr)):
            info_dict = ast.literal_eval(result_arr[i][2])
            monthly_price = float(
                info_dict['sub_price']) / int(info_dict['sub_duration'])
            total_price += monthly_price
            final_msg += f"{str(i + 1)}. {info_dict['sub_name']}   💵{str(round(monthly_price, 3))}$\n"

    await message.answer(f"Your monthly expenses 💸: <b>{round(total_price, 3)}$</b>\n\n{final_msg}", parse_mode="html")


def register_handler_info_statistics(dp: Dispatcher):
    dp.register_message_handler(info, commands=['info_sub'])
    dp.register_message_handler(statistics, commands=['statistics'])
