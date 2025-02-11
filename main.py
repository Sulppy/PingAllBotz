import asyncio
import logging
import sys
import handlers
from handlers import database, allping, superuser

from src.getchatu import init_pyrogram
from config_reader import config
from aiogram import Bot, Dispatcher

from src.initdb import init_db

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.tg_token.get_secret_value())


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    print("Initializing database...")
    init_db()
    print("Database initialized.")
    print("Initializing pyrogram...")
    await init_pyrogram() #Initialization Pyrogram
    print("Pyrogram initialized.")

    # Диспетчер
    print("Initializing handlers...")
    dp = Dispatcher()
    dp.include_routers(database.router)
    dp.include_routers(allping.router)
    dp.include_routers(superuser.router)
    print("Handler initialized.")
    # And the run events dispatching
    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot started.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
