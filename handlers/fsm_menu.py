from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot, ADMIN
from keyboards.client_kb import cancel_markup
from database import bot_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


async def fsm_start(message: types.Message):
    if message.from_user.id in ADMIN:
        await FSMAdmin.photo.set()
        await message.answer(f'Здравствуйте {message.from_user.full_name}'
                             f'Скиньте фотографию блюда',
                             reply_markup=cancel_markup)

    else:
        await message.reply('Пишите в лс')


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.answer('Напишите название блюда')


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        await FSMAdmin.next()
        await message.answer('Опишите блюдо')


async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        await FSMAdmin.next()
        await message.answer('цена блюда')


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
        await bot.send_photo(message.from_user.id, data['photo'],
                             caption=f"Name: {data['name']}\n"
                                     f"description: {data['description']}\n"
                                     f"price: {data['price']}")
    await bot_db.sql_command_insert(state)
    await state.finish()
    await message.answer("Все гуляй вася)")


async def cancel_registeration(message: types, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    else:
        await state.finish()
        await message.answer('Регистрация блюда отменена)')


async def delete_data(message: types.Message):
    if message.from_user.id in ADMIN and message.chat.type == "private":
        global users
        users = await bot_db.sql_command_all()
        for user in users:
            await bot.send_photo(message.from_user.id, user[0],
                                 caption=f"name: {user[1]}"
                                         f"description : {user[2]}"
                                         f"price: {user[3]} ",
                                 reply_markup=InlineKeyboardMarkup().add(
                                     InlineKeyboardButton(
                                         f"delete: {user[1]}",
                                         callback_data=f"delete {user[1]}"
                                     )
                                 )
                                 )

    else:
        await message.reply("Ты не мой Босс!")


async def complete_delete(call: types.CallbackQuery):
    await bot_db.sql_command_delete(call.data.replace('delete ', ""))
    await call.answer(text="Стерт с БД", show_alert=True)
    await bot.delete_message(call.message.chat.id, call.message.message_id)


def register_handler_fsmmenu(dp: Dispatcher):
    dp.register_message_handler(cancel_registeration, state='*', commands='cancel')
    dp.register_message_handler(cancel_registeration,
                                Text(equals='cancel', ignore_case=True), state='*')

    dp.register_message_handler(fsm_start, commands=['reg'])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo,
                                content_types=['photo'])
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(delete_data, commands=['del'])
    dp.register_callback_query_handler(
        complete_delete,
        lambda call: call.data and call.data.startswith("delete ")
    )
