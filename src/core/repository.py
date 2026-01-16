from sqlmodel import select
from sqlalchemy.orm import selectinload

from typing import List, Generic, TypeVar
from src.core.database import AsyncSession, BaseModel
import uuid

T = TypeVar('T', bound=BaseModel)

class BaseRepository(Generic[T]):
    def __init__(self, entity: T, db: AsyncSession, options: List[selectinload] = []):
        self.entity = entity
        self.db = db
        self.options: List[selectinload] = options

    async def get_all(self, sort_by: str = "created_at", sort_order: str = "asc") -> List[T]:
        stms = select(self.entity).options(*self.options)

        if sort_by and sort_order:
            stms = stms.order_by(getattr(self.entity, sort_by).asc() if sort_order == "asc" else getattr(self.entity, sort_by).desc())

        result = await self.db.execute(stms)
        return result.scalars().all()

    async def get_by_id(self, id: str) -> BaseModel:
        result = await self.db.execute(select(self.entity).where(self.entity.id == uuid.UUID(str(id))).options(*self.options))
        return result.scalars().first()

    async def get_one_by_id(self, id: str) -> BaseModel:
        result = await self.db.execute(select(self.entity).where(self.entity.id == uuid.UUID(str(id))).options(*self.options))
        return result.scalar_one()

    async def update(self, entity: T) -> T:
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def create(self, entity: T) -> T:
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity