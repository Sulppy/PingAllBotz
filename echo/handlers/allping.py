from Costil.getchatu import get_chat_members
from aiogram import Router, F
from aiogram.types import Message

router = Router()  # [1]


@router.message(F.text, F.text.contains("@all"))  # [2]
async def test(message: Message):
    members = []
    chatid = message.chat.id
    members = await get_chat_members(chatid)
    mess = []
    #for i in range(len(members)):
    #    mess.append("tg://user?"+members[i])
    await message.reply(f"Вы довольны своей работой? [all](tg://user?{members[0]})", parse_mode="Markdown")
