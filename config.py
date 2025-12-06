# config.py
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
DB_DSN = os.getenv("DB_DSN")

if not BOT_TOKEN:
    raise RuntimeError("Не задан BOT_TOKEN. Укажи его в .env или переменных окружения.")
if not DB_DSN:
    raise RuntimeError("Не задан DB_DSN. Укажи DB_DSN в .env или переменных окружения.")
