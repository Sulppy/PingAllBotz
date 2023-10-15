from pyrogram import Client
import config

api_id = config.PROG_ID
api_hash = config.PROG_HASH
bot_token = config.TG_TOKEN


async def get_chat_members(chat_id):
    app = Client("PyroBot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, in_memory=True)
    chat_members = []
    await app.start()
    async for member in app.get_chat_members(chat_id):
        chat_members = chat_members + [member.user.id]
    await app.stop()
    return chat_members
