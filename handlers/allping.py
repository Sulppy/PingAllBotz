import sqlite3
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from config_reader import config

router = Router()
router.message.filter(
    F.chat.type != "private"
)


@router.message(Command("allping"))
async def echo_message(message: Message):
    chatid = message.chat.id
    conn = sqlite3.connect(config.database_name.get_secret_value())
    cur = conn.cursor()
    cur.execute(f"SELECT user_id FROM chat_user WHERE chat_id = {chatid}")
    entry = cur.fetchone()
    conn.close()
    message_str = ""
    if entry is None:
       from src.getchatu import pyroadd
       await pyroadd(chatid)
    for i in entry:
        message_str += "[\u2060](tg://user?id=" + str(i) + ")"
    await message.reply(f"@{message.from_user.username} созывает всех!{message_str}", parse_mode="Markdown")





# @router.message(Command("test"))
# async def test(message: Message):
#     await botadd(message)
#     await message.answer("Testiiing")
