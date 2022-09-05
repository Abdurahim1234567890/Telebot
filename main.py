import random

from aiogram.utils import executor
from config import dp, URL, bot
from handlers import client, callbak, extra, admin, fsm_menu, natification, inline
from database import bot_db
import logging
import asyncio
from decouple import config


async def on_startup(_):
    await bot.set_webhook(URL)
    asyncio.create_task(natification.time())
    bot_db.sql_create()


async def on_shutdown(dp):
    await bot.delete_webhook()

inline.register_handler_inline(dp)
fsm_menu.register_handler_fsmmenu(dp)
client.register_handlers_client(dp)
callbak.register__handlers_callback(dp)

admin.register_handler_admin(dp)
natification.register_hendler_notification(dp)


extra.register_handler_extra(dp)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    executor.start_webhook(
        dispatcher=dp,
        webhook_path="",
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host='0.0.0.0',
        port=config("PORT", default=5000)
    )

#2