import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

import db_models
# Імпортуємо моделі
from db_models import Base

# Підключення до бази даних
engine = create_async_engine(db_models.DATABASE_URL, poolclass=pool.NullPool)

# Налаштування логів Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# Асинхронний режим міграції
async def run_migrations():
    async with engine.begin() as conn:
        await conn.run_sync(target_metadata.create_all)

    async with engine.begin() as conn:
        await conn.run_sync(context.configure, connection=conn)
        await conn.run_sync(context.run_migrations)


async def main():
    await run_migrations()


if __name__ == "__main__":
    asyncio.run(main())
