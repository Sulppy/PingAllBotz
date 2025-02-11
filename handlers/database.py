import sqlite3
from config_reader import config
from src.getchatu import get_chat_members
from aiogram import Router, F
from aiogram.filters import ChatMemberUpdatedFilter, Command, JOIN_TRANSITION, IS_MEMBER, IS_NOT_MEMBER, IS_ADMIN
from aiogram.types import Message, ChatMemberUpdated
from aiogram.methods import GetChatMember, GetChat, GetChatMemberCount
from main import bot

router = Router()  # [1]

ADMIN_ID = config.admin_id.get_secret_value()

# Сокращение фильтра проверки типа чата
IS_PRIVATE = F.chat.type == "private"
NOT_PRIVATE = F.chat.type != "private"

# Название файла бд
bd = config.database_name.get_secret_value()


# При присоединении просим админку, если её нет, а если есть, то парсим данные
@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION), NOT_PRIVATE)
async def botadd(member: ChatMemberUpdated):
    admin = await bot(GetChatMember(chat_id=member.chat.id, user_id=member.new_chat_member.user.id))
    if admin.status == "administrator":
        await botadmin(member)
    else:
        await member.answer("Для дальнейшей работы мне необходима админка\nНе могли бы вы её выдать? 🥺")


# Как только получили админку запускаем парсинг
@router.my_chat_member(ChatMemberUpdatedFilter(IS_ADMIN), NOT_PRIVATE)
async def botadmin(member: ChatMemberUpdated):
    conn = sqlite3.connect(bd)
    cur = conn.cursor()
    await member.answer("Дайте пару секунд и всё будет готово")
    chatid = member.chat.id
    # Проверка, есть ли этот чат в таблице чатов
    cur.execute(f"SELECT * FROM chats WHERE chat_id = {chatid}")
    result = cur.fetchone()
    # Если нет, то добавляем новую строку со значениями
    if result is None:
        cur.execute(f"INSERT INTO chats VALUES ({chatid}, '{member.chat.title}', '{member.chat.type}')")
        conn.commit()
    # Подготовка к проверке совпадений пользователей, чтобы лишний раз не тормошить pyrogram и не словить FloodWait
    memcount = await bot(GetChatMemberCount(chat_id=member.chat.id))
    cur.execute(f"SELECT user_id FROM users WHERE chat_id = {chatid}")
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
    await member.answer("Готов к работе!")
    conn.close()

# На случай, если в бд не во всех чатах проставились типы чата
@router.message(Command("addchats_type"), IS_PRIVATE)
async def add_chattype():
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
@router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER), NOT_PRIVATE)
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