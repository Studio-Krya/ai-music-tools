from fastapi import Depends
from typing import List

from src.core.database import async_get_db, AsyncSession
from .models import User
from .dtos import UserCreate
from sqlmodel import select

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[User]:
        users = await self.db.execute(select(User))
        return users.scalars().all()

    async def create(self, user: UserCreate) -> User:
        user = User(name=user.name, age=user.age)
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

def get_user_service(db: AsyncSession = Depends(async_get_db)) -> UserService:
    return UserService(db)