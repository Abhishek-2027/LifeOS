"""Initialize the production PostgreSQL database by creating tables.

Usage:
    python scripts/init_postgres.py --database-url postgresql+asyncpg://user:pass@host:5432/lifeos

This will import the SQLAlchemy `Base` and run `create_all` in a synchronous context
for ease of bootstrap. For production migrations, use Alembic.
"""
import argparse
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.models import Base

async def main(database_url: str):
    engine = create_async_engine(database_url, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--database-url', required=True, help='Async DB URL')
    args = p.parse_args()
    asyncio.run(main(args.database_url))
