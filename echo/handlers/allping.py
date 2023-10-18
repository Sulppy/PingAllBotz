from Costil.getchatu import get_chat_members
from aiogram import Router, F, Bot, Dispatcher
from aiogram.types import Message
from config import TG_TOKEN

router = Router()  # [1]


@router.message(F.text, F.text.contains("@all"))
async def echo_message(message: Message):
    chatid = message.chat.id
    members = await get_chat_members(chatid)
    mention = []
    for i in range(len(members)):
        mention.append("[\u2060](tg://user?id=" + str(members[i]) + ")")
    mess_str = "".join(mention)
    await message.reply(f"Pinged{mess_str}", parse_mode="Markdown")
