import sqlite3
from config_reader import config

bd = config.database_name.get_secret_value()

def init_db():
    conn = sqlite3.connect(bd)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS chat("
                "id INTEGER PRIMARY KEY,"
                "invited_user_id INTEGER NOT NULL);")
    cur.execute("CREATE TABLE IF NOT EXISTS chat_user("
                "user_id INTEGER NOT NULL, "
                "chat_id INTEGER NOT NULL, "
                "PRIMARY KEY (user_id, chat_id),"
                "CONSTRAINT fk_chat_id FOREIGN KEY (chat_id) REFERENCES chat(id));"
                )
    conn.commit()
    conn.close()

def check_chat(chatid: int):
    conn = sqlite3.connect(bd)
    cur = conn.cursor()
    cur.execute(f"SELECT chat_id FROM chat WHERE chat_id = {chatid};")
    result = cur.fetchone()
    return result is not None