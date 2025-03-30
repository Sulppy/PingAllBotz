from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from src.database import conn

router = Router()
router.message.filter(
    F.chat.type != "private"
)


@router.message(Command("all"))
async def ping_all(message: Message):
    chatid = message.chat.id
    cur = conn.cursor()
    cur.execute(f"SELECT user_id FROM chat_user WHERE chat_id = {chatid}")
    entry = cur.fetchone()
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
