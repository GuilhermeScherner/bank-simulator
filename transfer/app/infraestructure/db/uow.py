from sqlalchemy.ext.asyncio import AsyncSession
from __future__ import annotations
from functools import cached_property


class UnitOfWork:
    def __init__(self, async_session: AsyncSession) -> None:
        self.async_session = async_session

    def __enter__(self) -> UnitOfWork:
        return self

    def __exit__(self, exec_type, exec_value, exec_traceback) -> None:
        if exec_type:
            self.rollback()
        else:
            self.commit()

    def rollback(self) -> None:
        self.async_session.rollback()

    def commit(self) -> None:
        self.async_session.commit()

    @cached_property
    def transfer(self) -> TransferRepository:
        return TransferRepository(self.session)
