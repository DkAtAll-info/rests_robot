# handlers/start.py
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.enums import ChatType  # <-- ВАЖНО: из aiogram.enums

def setup_start_router(dm) -> Router:
    router = Router(name="start")

    @router.message(CommandStart(), F.chat.type == ChatType.PRIVATE)
    async def cmd_start_private(message: Message):
        await dm.upsert_user(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
        )
        await message.answer(
            "👋 Привет!\n\n"
            "Этот бот был создан для того,\n"
            "чтобы автоматизировать ресты\n"
            "в группе @tg_chat45\n"
            "Чтобы увидеть список команд,\n"
            "введите /commands"
        )

    @router.message(CommandStart())
    async def cmd_start_in_group(message: Message):
        await message.reply("Команда /start предназначена для личных сообщений. Напишите мне в ЛС.")

    return router
