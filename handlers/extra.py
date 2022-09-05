import random

from aiogram import types, Dispatcher
from config import bot, dp, ADMIN


# @dp.message_handler()
async def echo(message: types.Message):

    bad_words = ["лох", "петух", "дурак ", "чорт", "жидкий"]
    username = f"@{message.from_user.username}" if message.from_user.username is not None else ""
    if message.text.lower() in bad_words:
        await bot.send_message(
            message.chat.id,
            f"не матерись мал {message.from_user.full_name},"
            f"сам ты {message.text} {username} "
        )
        await bot.delete_message(message.chat.id, message.message_id)
    else:
        if message.text.startswith("game") and message.from_user.id in ADMIN:
            lst = ['⚽️', '🏀', '🎰', '🎳' '🎯']
            a = random.choice(lst)
            await bot.send_dice(message.chat.id, emoji=a)
        elif message.text.isdigit():
            await bot.send_message(message.chat.id, int(message.text) * int(message.text))
        else:
            await bot.send_message(message.chat.id, message.text)


def register_handler_extra(dp: Dispatcher):
    dp.register_message_handler(echo)
