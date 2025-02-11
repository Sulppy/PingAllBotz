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

# функция по добавлению пользователей в бд
async def pyroadd(chatid):
    conn = sqlite3.connect(bd)
    cur = conn.cursor()
    members = await get_chat_members(chatid)
    cur.execute(f"SELECT * FROM chat_user WHERE chat_id = {chatid};")
    entry = cur.fetchone()
    # Добавляем пользователей, которые есть в чате, в бд и к каждому пользователю сразу создается ссылка на пинг
    for i in members:
        # С помощью метода GetChatMember берутся все данные пользователя
        user = await bot(GetChatMember(chat_id=chatid, user_id=i))
        # Исключаем ботов из добавления в бд
        if (not entry.contains(i)) and (user.user.is_bot is False):
            cur.execute(f"INSERT INTO chat_user VALUES {i}, {chatid};")
            conn.commit()
    conn.close()

async def check_user_member(chatid):
    conn = sqlite3.connect(bd)
    cur = conn.cursor()
    memcount = await bot(GetChatMemberCount(chat_id=chatid))
    cur.execute(f"SELECT user_id FROM chat_user WHERE chat_id = {chatid}")
    result = cur.fetchall()
    userids = [i[0] for i in result]
    # сравниваем количество для ускорения работы
    if memcount == range(len(userids)):
        # проходимся по каждому юзеру, если кого-то нет, то запускаем полную проверку с 0
        for i in userids:
            user = await bot(GetChatMember(chat_id=chatid, user_id=i))
            if user.status is not str(IS_MEMBER):
                await pyroadd(chatid)
                break
    else:
        await pyroadd(chatid)
