from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.markdown import hbold

from config import bot
from keyboards.client_kb import start_markup
from database.bot_db import sql_command_random
from perser.fighter import parser


# @dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await bot.send_message(message.chat.id,
                           f"Здравствй Путник!!!\n {message.from_user.full_name}")


# @dp.message_handler(commands=['help'])
async def start_handlers(message: types.Message):
    await bot.send_message(message.chat.id,
                           f"для начало работы пропишите: /start  /quiz  /mems /fighter !pin game  /напомни "
                           f"{message.from_user.full_name}")


# @dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT", callback_data='button_call_1')
    markup.add(button_call_1)

    question = "До 1923 года как назывался турецкий город Стамбул?"
    answers = [
        "Константинопаль",
        "Москва",
        "Бишкек",
        "Сеул",
        "Гонконг"

    ]
    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        open_period=10,
        explanation="мда...",
        reply_markup=markup
    )


async def pin(message: types.Message):
    if message.reply_to_message:
        await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
    else:
        await bot.send_message(message.chat.id, 'Это должно ответом на сообщение')


async def show_random_user(message: types.Message):
    await sql_command_random(message)


async def parser_fighter(message: types.Message):
    data = parser()
    for item in data:
        title = hbold(item['title'])
        await bot.send_message(
            message.from_user.id,
            f"{item['link']}\n\n"
            f"{item['title']}\n"
            f"#{item['year']}\n"
            f"#{item['city']}\n"
            f"#{item['genre']}\n"
        )

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
    dp.register_message_handler(start_handlers, commands=["help"])
    dp.register_message_handler(quiz_1, commands=['quiz'])
    dp.register_message_handler(pin, commands=['pin'], commands_prefix='!')
    dp.register_message_handler(show_random_user, commands=['get'])
    dp.register_message_handler(parser_fighter, commands=['fighter'])
 