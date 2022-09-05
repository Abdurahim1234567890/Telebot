from aiogram import Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start = KeyboardButton("/start")
quiz = KeyboardButton("/quiz")
location_button = KeyboardButton("Share location", request_location=True)
info_butoon = KeyboardButton("Share info", request_contact=True)

start_markup = ReplyKeyboardMarkup(resize_keyboard=True,
                                   one_time_keyboard=True)

start_markup.row(start, quiz)
start_markup.add(location_button, info_butoon)

cancel_button = KeyboardButton("CANCEL")
cancel_markup = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
).add(cancel_button)


def register_handlers_client(dp: Dispatcher, start_handlers=None):
    dp.register_message_handler(start_handlers, commands=['start'])
    dp.register_message_handler(start_handlers, commands=['help'])
    dp.register_message_handler(quiz, commands=['quiz'])
    dp.register_message_handler(start_handlers, commands=['cancel'])

