import ast
from aiogram import Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import Database

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


def register_handler_info(dp: Dispatcher):
    dp.register_message_handler(info, commands=['info_sub'])
