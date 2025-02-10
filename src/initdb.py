import sqlite3
from config_reader import config

bd = config.database_name.get_secret_value()

def init_db():
    conn = sqlite3.connect(bd)
    cur = conn.cursor()
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
    conn.close()