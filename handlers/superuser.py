from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from config_reader import config

router = Router()
ADMIN_ID = config.admin_id.get_secret_value()
IS_USER_ADMIN = F.from_user.id.in_(ADMIN_ID)

# Сокращение фильтра проверки типа чата
IS_PRIVATE = F.chat.type == "private"
NOT_PRIVATE = F.chat.type != "private"

# Название файла бд
bd = config.database_name.get_secret_value()

@router.message(Command("getuserid"), IS_PRIVATE)
async def get_id(message: Message):
    await message.answer(f"{message.from_user.id}")