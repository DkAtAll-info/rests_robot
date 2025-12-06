# handlers/__init__.py
from aiogram import Router
from .start import setup_start_router

def setup_handlers(dm) -> Router:  # тип можно не указывать, чтобы избежать лишних импортов
    root = Router()
    root.include_router(setup_start_router(dm))
    return root
