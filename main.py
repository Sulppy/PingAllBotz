import asyncio
import logging
import sys
from handlers import allping, dbinit
from config_reader import config
from aiogram import Bot, Dispatcher

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.tg_token.get_secret_value())


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls

    # Диспетчер
    dp = Dispatcher()
    dp.include_routers(dbinit.router)
    dp.include_routers(allping.router)
    # And the run events dispatching
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
