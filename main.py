import asyncio
import logging
from aiogram import Bot, Dispatcher
from src.config import settings
from src.db import create_tables
from src.handlers.common import common_router
from src.handlers.game import quiz_router


logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=settings.API_TOKEN)
    dp = Dispatcher()

    # Роутеры
    dp.include_router(common_router)
    dp.include_router(quiz_router)

    # Инициализация БД
    await create_tables()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())