import asyncio
import aioschedule
from aiogram import types, Dispatcher

from config import bot


async def get_chat_id(message: types.Message):
    global chat_id
    chat_id = message.from_user.id
    await bot.send_message(chat_id=chat_id, text="oky!")


async def go_to_nature():
    await bot.send_message(chat_id=chat_id, text='Пора на природу!')


async def get_up():
    photo = open("media\\123.jpg", 'rb')
    await bot.send_photo(chat_id=chat_id, photo=photo,
                             caption="Горы ждууут")


async def time():
    aioschedule.every().wednesday.at("8:00").do(go_to_nature)
    aioschedule.every().wednesday.at("8:00").do(get_up)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(2)


def register_hendler_notification(dp: Dispatcher):
    dp.register_message_handler(get_chat_id,
                                lambda word: "Напомни по братски" in word.text)
