from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot, dp
import random


# @dp.callback_query_handler(lambda call: call.data == "button_call_1")
async def quiz_2(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button_call_2 = InlineKeyboardButton("NEXT", callback_data='button_call_2')
    markup.add(button_call_2)
    question = "Сколько полос на флаге США?"
    answers = [
        "0",
        "9",
        "13",
        "2",
        "11",
        "7",

    ]
    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=2,
        open_period=10,
        explanation="мда...",
        reply_markup=markup
    )


# @dp.callback_query_handler(lambda call: call.data == "button_call_2")
async def quiz_3(call: types.CallbackQuery):
    markup = InlineKeyboardMarkup()
    button_call_27 = InlineKeyboardButton("Next ", callbak_data='button_call_27')
    markup.add(button_call_27)

    question = "Почему Нидерланды называют Голландией?"
    answers = [
        "Засидеть Моча",
        "имя носит только одна из провинций, а не вся страна",
        "Спокойный Упомянуть",
        "Пенопласт Подпираться",
        "Полюбоваться Совместный"
    ]
    await bot.send_poll(
        chat_id=call.message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=1,
        open_period=60,
        explanation="Ой бой ты че?",
    )


# @dp.message_handler(commands=['mems'])
async def start_handler(message: types.Message):
    lst = ["media/memm.jpg", "media/hr_to_dev.jpg"]
    photo = open(random.choice(lst), 'rb')
    await bot.send_photo(message.chat.id, photo=photo)


def register__handlers_callback(dp: Dispatcher):
    dp.register_callback_query_handler(quiz_2, lambda call: call.data == "button_call_1")
    dp.register_callback_query_handler(quiz_3, lambda call: call.data == "button_call_2")
    dp.register_message_handler(start_handler, commands=["mems"])



