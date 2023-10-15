import asyncio
import logging
import sys
from echo.handlers import allping
from config import TG_TOKEN
from aiogram import Bot, Dispatcher

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls

    # Диспетчер
    dp = Dispatcher()
    bot = Bot(token=TG_TOKEN)
    dp.include_routers(allping.router)
    # And the run events dispatching
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
