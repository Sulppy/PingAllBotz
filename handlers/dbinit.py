import sqlite3
from Costil.getchatu import get_chat_members
from aiogram import Router, F
from aiogram.filters import ChatMemberUpdatedFilter, Command, JOIN_TRANSITION, LEAVE_TRANSITION
from aiogram.types import Message, ChatMemberUpdated
from aiogram.methods import GetChatMember, GetChat
from main import bot

router = Router()  # [1]

# Сокращение фильтра проверки типа чата
IS_PRIVATE = F.chat.type == "private"
NOT_PRIVATE = F.chat.type != "private"

# Название файла бд
bd = 'data.sqlite'


@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION), NOT_PRIVATE)
async def botadd(message: Message):
    conn = sqlite3.connect(bd)
    cur = conn.cursor()
    # Если её нет, то создается таблица чатов
    cur.execute("CREATE TABLE IF NOT EXISTS chats("
                "chat_id INTEGER NOT NULL PRIMARY KEY, "
                "chat_title TEXT, "
                "chat_type TEXT NOT NULL)"
                )
    conn.commit()
    # Если её нет, то создаётся таблица юзеров
    cur.execute("CREATE TABLE IF NOT EXISTS users("
                "user_id INTEGER NOT NULL, "
                "user_name TEXT, "
                "url_ping TEXT NOT NULL, "
                "chat_id INTEGER NOT NULL)"
                )
    conn.commit()
    chatid = message.chat.id
    # Проверка, есть ли этот чат в таблице чатов
    cur.execute(f"SELECT * FROM chats WHERE chat_id = {chatid}")
    entry = cur.fetchone()
    # Если нет, то добавляем новую строку со значениями
    if entry is None:
        cur.execute(f"INSERT INTO chats VALUES ({chatid}, '{message.chat.title}', '{message.chat.type}')")
        conn.commit()
    members = await get_chat_members(chatid)
    # Добавляем пользователей, которые есть в чате, в бд и к каждому пользователю сразу создается ссылка на пинг
    for i in members:
        cur.execute(f"SELECT * FROM users WHERE chat_id = {chatid} AND user_id = {i}")
        entry = cur.fetchone()
        # С помощью метода GetChatMember берутся все данные пользователя
        user = await bot(GetChatMember(chat_id=chatid, user_id=i))
        # Исключаем ботов из добавления в бд
        if (entry is None) and (user.user.is_bot is False):
            url = "[\u2060](tg://user?id=" + str(i) + ")"
            cur.execute(f"INSERT INTO users VALUES ({i}, '{user.user.username}', '{url}', {chatid})")
            conn.commit()
    conn.close()


# Если бот не сработал на добавление, то можно использовать эту команду в чате, чтобы запарсить данные
@router.message(Command("add"), NOT_PRIVATE)
async def add_db(message: Message):
    await botadd(message)
    await message.answer("Добавлено!")


# На случай, если в бд не во всех чатах проставились типы чата
@router.message(Command("addchats_type"), IS_PRIVATE)
async def add_chattype(message: Message):
    conn = sqlite3.connect(bd)
    cur = conn.cursor()
    cur.execute(f"SELECT chat_id FROM chats")
    result = cur.fetchall()
    chatid = [i[0] for i in result]
    for i in chatid:
        chat = await bot(GetChat(chat_id=i))
        cur.execute(f"UPDATE chats SET chat_title='{chat.title}', chat_type='{chat.type}' WHERE chat_id = {i};")
        conn.commit()
    conn.close()


# Если пользователь выходит из чата, то удаляем его и из бд (может сработать и на выход бота, так что фильтруем)
@router.chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION), NOT_PRIVATE)
async def delmem(member: ChatMemberUpdated):
    chatid = member.chat.id
    user = member.new_chat_member.user
    if user.is_bot is False:
        conn = sqlite3.connect(bd)
        cur = conn.cursor()
        cur.execute(f"DELETE FROM users WHERE chat_id = {chatid} AND user_id = {user.id}")
        conn.commit()
        conn.close()


# Если пользователь присоединяется к чату, то его автоматом закидывает в бд
@router.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION), NOT_PRIVATE)
async def addmem(member: ChatMemberUpdated):
    chatid = member.chat.id
    user = member.new_chat_member.user
    conn = sqlite3.connect(bd)
    cur = conn.cursor()
    cur.execute(f"SELECT user_id, chat_id FROM users WHERE user_id = {user.id} AND chat_id = {chatid}")
    result = cur.fetchone()
    if (user.is_bot is False) and (result is None):
        url = "[\u2060](tg://user?id=" + str(user.id) + ")"
        cur.execute(f"INSERT INTO users VALUES ({user.id}, '{user.username}', '{url}', {chatid})")
        conn.commit()
    conn.close()
