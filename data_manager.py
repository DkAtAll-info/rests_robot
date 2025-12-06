
# data_manager.py
import asyncpg
import ssl
from typing import Optional

class DataManager:
    def __init__(self, dsn: str):
        self._dsn = dsn
        self._pool: Optional[asyncpg.Pool] = None

    async def init_pool(self):
        """Создаёт пул соединений (Neon требует SSL)."""
        ctx = ssl.create_default_context()
        ctx.check_hostname = True
        ctx.verify_mode = ssl.CERT_REQUIRED

        self._pool = await asyncpg.create_pool(dsn=self._dsn, ssl=ctx, min_size=1, max_size=5)

    async def close_pool(self):
        if self._pool:
            await self._pool.close()

    async def ensure_schema(self):
        """Создаёт таблицы, если их нет."""
        assert self._pool is not None, "Pool is not initialized"
        async with self._pool.acquire() as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id     BIGINT PRIMARY KEY,
                    first_name  TEXT,
                    last_name   TEXT,
                    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
                );
            """)

    async def upsert_user(self, user_id: int, first_name: str | None, last_name: str | None):
        """Добавляет/обновляет пользователя."""
        assert self._pool is not None, "Pool is not initialized"
        async with self._pool.acquire() as conn:
            await conn.execute("""
                INSERT INTO users (user_id, first_name, last_name)
                VALUES ($1, $2, $3)
                ON CONFLICT (user_id)
                DO UPDATE SET
                    first_name = EXCLUDED.first_name,
                    last_name  = EXCLUDED.last_name,
                    updated_at = now();
            """, user_id, first_name, last_name)
