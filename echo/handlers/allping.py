from typing import Union
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, ChatMemberOwner, ChatMemberAdministrator, ChatMemberMember, Chat
from aiogram.methods import GetChatMember, GetChat
from aiogram.types.bot_command_scope_chat_member import BotCommandScopeChatMember

router = Router()  # [1]


@router.message(F.text, F.text.contains("@all"))  # [2]
async def test(message: Message):
    # mem = bot(GetChatMember())
    ll = {id: ['12345', '423412']}
    chat_members = await Bot.get_chat_member(message.chat.id)
    user_ids = [member.user.id for member in chat_members]
    #oal = BotCommandScopeChatMember()
    #mem: Union[ChatMemberOwner, ChatMemberAdministrator, ChatMemberMember] = await GetChatMember(chat_id=chatid.id)
    await message.reply(f"Вы довольны своей работой? userid={ll[id]}", parse_mode="Markdown")
