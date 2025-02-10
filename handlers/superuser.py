from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from config_reader import config

router = Router()
ADMIN_ID = config.admin_id.get_secret_value()

# Сокращение фильтра проверки типа чата
IS_PRIVATE = F.chat.type == "private"
NOT_PRIVATE = F.chat.type != "private"

@router.message(Command("getid"), IS_PRIVATE)
async def get_id(message: Message):
    await message.answer(f"{message.from_user.id}")