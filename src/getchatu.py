import asyncio
from pyrogram import Client
from pyrogram.errors.exceptions.flood_420 import FloodWait
from config_reader import config

api_id = config.prog_id.get_secret_value()
api_hash = config.prog_hash.get_secret_value()
bot_token = config.tg_token.get_secret_value()

FloodWait()
app = Client("PyroBot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, in_memory=True)

async def init_pyrogram():
    try:
        await app.start()
        await asyncio.sleep(5)
    except FloodWait as e:
        await asyncio.sleep(e.value)


async def get_chat_members(chat_id):
    chat_members = []
    async for member in app.get_chat_members(chat_id):
        chat_members.append(member.user.id)
    await app.stop()
    return chat_members
