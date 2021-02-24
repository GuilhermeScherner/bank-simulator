from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.db.database import engine
from app.infraestructure.db.uow import UnitOfWork


async def get_uow() -> Generator:
    session = AsyncSession(engine)
    try:
        yield UnitOfWork(session)
    finally:
        await session.close()