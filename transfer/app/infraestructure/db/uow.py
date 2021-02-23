from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from functools import cached_property
from app.infraestructure.repositories.transfer import TransferRepository


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def __aenter__(self) -> UnitOfWork:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    @cached_property
    def transfer(self) -> TransferRepository:
        return TransferRepository(self.session)
