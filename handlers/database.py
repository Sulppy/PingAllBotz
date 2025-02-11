import sqlite3
from config_reader import config
from src.getchatu import get_chat_members, pyroadd
from aiogram import Router, F
from aiogram.filters import ChatMemberUpdatedFilter, Command, JOIN_TRANSITION, IS_MEMBER, IS_NOT_MEMBER, IS_ADMIN
from aiogram.types import ChatMemberUpdated
from aiogram.methods import GetChatMember, GetChat, GetChatMemberCount
from main import bot
from src.initdb import check_chat

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
    add_user = member.from_id
    chatid = member.chat.id
    admin = await bot(GetChatMember(chat_id=member.chat.id, user_id=member.new_chat_member.user.id))
    # Проверка, есть ли этот чат в таблице чатов
    conn = sqlite3.connect(bd)
    cur = conn.cursor()
    if check_chat(chatid) is None:
        cur.execute(f"INSERT INTO chat VALUES ({chatid}, {add_user});")
        conn.commit()
    else:
        cur.execute(f"UPDATE chat SET invited_user_id={add_user} WHERE chat_id = {chatid};")
        conn.commit()
    conn.close()
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

# Если пользователь выходит из чата, то удаляем его и из бд (может сработать и на выход бота, так что фильтруем)
@router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER), NOT_PRIVATE)
async def delmem(member: ChatMemberUpdated):
    chatid = member.chat.id
    user = member.new_chat_member.user
    if user.is_bot is False:
        conn = sqlite3.connect(bd)
        cur = conn.cursor()
        cur.execute(f"DELETE FROM chat_user WHERE chat_id = {chatid} AND user_id = {user.id};")
        conn.commit()
        conn.close()


# Если пользователь присоединяется к чату, то его автоматом закидывает в бд
@router.chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION), NOT_PRIVATE)
async def addmem(member: ChatMemberUpdated):
    chatid = member.chat.id
    user = member.new_chat_member.user
    if user.is_bot is False:
        conn = sqlite3.connect(bd)
        cur = conn.cursor()
        cur.execute(f"SELECT user_id, chat_id FROM user WHERE user_id = {user.id} AND chat_id = {chatid};")
        result = cur.fetchone()
        if (user.is_bot is False) and (result is None):
            cur.execute(f"INSERT INTO chat_user VALUES ({user.id}, {chatid});")
            conn.commit()
        conn.close()