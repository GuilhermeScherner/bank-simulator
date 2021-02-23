from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.mappings.transfer import Users
from app.infraestructure.repositories.base import BaseRepository


class TransferRepository(BaseRepository[Users]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, AsyncSession)