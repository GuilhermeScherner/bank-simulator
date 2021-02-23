from typing import Generic, Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.mappings.base import BaseModel

MappingType = TypeVar("MappingType", bound=BaseModel)


class BaseRepository(Generic[MappingType]):
    def __init__(self, db: AsyncSession, mapping: Type[MappingType]):
        self.db = db
        self.mapping = mapping

    async def create(self, obj: MappingType) -> MappingType:
        self.db.add(obj)
        await self.db.flush([obj])
        return obj

