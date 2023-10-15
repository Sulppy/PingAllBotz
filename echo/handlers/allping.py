from Costil.getchatu import get_chat_members
from aiogram import Router, F
from aiogram.types import Message

router = Router()  # [1]


@router.message(F.text, F.text.contains("@all"))  # [2]
async def test(message: Message):
    members = []
    chatid = message.chat.id
    members = await get_chat_members(chatid)
    await message.reply(f"Вы довольны своей работой? [all](tg://user?id={members})", parse_mode="Markdown")
