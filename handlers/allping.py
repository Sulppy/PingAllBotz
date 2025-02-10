import sqlite3
from handlers.database import botadmin
from aiogram import Router, F
from aiogram.types import Message

router = Router()
router.message.filter(
    F.chat.type != "private"
)


@router.message(F.text, F.text.contains("@all"))
async def echo_message(message: Message):
    chatid = message.chat.id
    conn = sqlite3.connect('data.sqlite')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM chats WHERE chat_id = {chatid}")
    entry = cur.fetchone()
    if entry is None:
        await message.answer(f"Похоже, что я впервые в этом чате, подождите немного ☺️")
        await botadmin(message)
    cur.execute(f"SELECT url_ping FROM users WHERE chat_id = {chatid}")
    members = cur.fetchall()
    mention = [i[0] for i in members]
    mess_str = "".join(mention)
    await message.reply(f"@{message.from_user.username} созывает всех!{mess_str}", parse_mode="Markdown")
    conn.close()





# @router.message(Command("test"))
# async def test(message: Message):
#     await botadd(message)
#     await message.answer("Testiiing")
