import sqlite3
import random

from config import bot


def sql_create():
    global db, cursor
    db = sqlite3.connect("bot.sqlite3")
    cursor = db.cursor()

    if db:
        print("База данных подключена!!!")

    db.execute("CREATE TABLE IF NOT EXISTS menus"
               "(photo TEXT, name TEXT PRIMARY KEY,"
               "description TEXT, price INTEGER)")

    db.commit()


async def sql_command_insert(state):
    async with state.proxy() as menu:
        cursor.execute("INSERT INTO menus VALUES "
                       "(?,?,?,?)",
                       tuple(menu.values()))
        db.commit()


async def sql_command_random(message):
    result = cursor.execute("SELECT *  FROM menus ").fetchall()
    random_user = random.choice(result)
    await bot.send_photo(message.from_user.id, random_user[0],
                         caption=f"name: {random_user[1]} \n"
                                 f"description : {random_user[2]} \n"
                                 f"price: {random_user[3]} ")


async def sql_command_all():
    return cursor.execute("SELECT * FROM menus").fetchall()


async def sql_command_delete(id):
    cursor.execute("DELETE FROM menus WHERE name == ?", (id,))
    db.commit()
