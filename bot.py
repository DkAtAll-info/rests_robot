# bot.py
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# ⬇️ Загружаем .env ПЕРЕД импортом config (чтобы os.getenv уже видел переменные)
from dotenv import load_dotenv
if os.path.exists(os.path.join(os.path.dirname(__file__), ".env")):
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

from config import BOT_TOKEN, DB_DSN
from data_manager import DataManager
from handlers import setup_handlers

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

async def main():
    dm = DataManager(dsn=DB_DSN)
    await dm.init_pool()
    await dm.ensure_schema()

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(setup_handlers(dm))

    me = await bot.get_me()
    logging.info("✅ Бот @%s запущен. Ожидание обновлений...", me.username)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await dm.close_pool()
        logging.info("⏹️ Остановка бота и закрытие соединений с БД")

if __name__ == "__main__":
    asyncio.run(main())
