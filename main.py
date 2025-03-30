import asyncio
import logging
import sys

from pyrogram.utils import ainput

from handlers import database, allping, superuser

from src.config_reader import config
from aiogram import Bot, Dispatcher

from src.database import init_db, conn

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.tg_token.get_secret_value())

class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    print("Initializing database...")
    init_db()
    print("Database initialized.")
    print("Initializing pyrogram...")
    from src.getchatu import init_pyrogram, stop_pyrogram
    await init_pyrogram() #Initialization Pyrogram
    print("Pyrogram initialized.")
    # Диспетчер
    print("Initializing handlers...")
    dp = Dispatcher()
    dp.include_routers(database.router)
    dp.include_routers(allping.router)
    dp.include_routers(superuser.router)
    print("Handler initialized.")
    print("Bot started.")
    async def console_input():
        while True:
            x = await ainput()
            x = x.strip()
            if x in {"exit", "quit", "q"}:
                print("Stopping bot...")
                await dp.stop_polling()
                break
            else:
                print(f"{BColors.WARNING}Неверная команда.{BColors.ENDC}")
    console_task = asyncio.create_task(console_input())
    await dp.start_polling(bot, skip_updates=True)
    await console_task
    await stop_pyrogram()
    conn.close()
    print("Bot stopped.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        from src.getchatu import stop_pyrogram, app
        if app.is_initialized:
            loop.run_until_complete(app.stop())  # Убеждаемся, что Pyrogram остановлен
        loop.close()
