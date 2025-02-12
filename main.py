import asyncio
import logging
import sys

from handlers import database, allping, superuser

from config_reader import config
from aiogram import Bot, Dispatcher

from src.initdb import init_db

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
    from src.getchatu import init_pyrogram
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
    async def thread():
        while True:
            x = input()
            if x in {"exit", "quit", "q"}:
                await dp.stop_polling()
                break
            else:
                print(f"{BColors.WARNING}Неверная команда.{BColors.ENDC}")
    asyncio.create_task(thread())
    await dp.start_polling(bot)
    print("Bot stopped.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
