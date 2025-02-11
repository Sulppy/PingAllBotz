from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from config_reader import config
from handlers.database import botadmin

router = Router()
ADMIN_ID = config.admin_id.get_secret_value()
IS_USER_ADMIN = F.from_user.id == ADMIN_ID

# Сокращение фильтра проверки типа чата
IS_PRIVATE = F.chat.type == "private"
NOT_PRIVATE = F.chat.type != "private"

@router.message(Command("getuserid"), IS_PRIVATE)
async def get_id(message: Message):
    await message.answer(f"{message.from_user.id}")

# Если бот не сработал на добавление, то можно использовать эту команду в чате, чтобы запарсить данные
# Только для личного пользования!!!
@router.message(Command("add"), NOT_PRIVATE, IS_USER_ADMIN)
async def add_db(message: Message):
    await botadmin(message)
