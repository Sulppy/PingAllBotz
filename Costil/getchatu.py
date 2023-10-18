import asyncio
import pyrogram
from pyrogram import Client, enums
from pyrogram.errors.exceptions.flood_420 import FloodWait
import config

api_id = config.PROG_ID
api_hash = config.PROG_HASH
bot_token = config.TG_TOKEN

FloodWait()


async def get_chat_members(chat_id):
    app = Client("PyroBot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, in_memory=True)
    try:
        await app.start()
        await asyncio.sleep(3)
    except FloodWait as e:
        await asyncio.sleep(e.value)
    chat_members = []
    async for member in app.get_chat_members(chat_id):
        chat_members.append(member.user.id)  # TODO Ошибка, неверно вставляются данные (join или append)
    await app.stop()
    return chat_members
