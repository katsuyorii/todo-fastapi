from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import TypeVar


T = TypeVar('T')


class DatabaseBaseRepository:
    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    async def get_all(self, skip: int = 0, limit: int = 5) -> list[T]:
        result = await self.session.execute(select(self.model).offset(skip).limit(limit))

        return result.scalars().all()
    
    async def get(self, id: int) -> T | None:
        result = await self.session.execute(select(self.model).where(self.model.id == id))

        return result.scalar_one_or_none()
    
    async def create(self, obj_dict: dict) -> T:
        obj = self.model(**obj_dict)

        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)

        return obj
    
    async def update(self, obj: T, updated_obj_dict: dict) -> T:
        for key, value in updated_obj_dict.items():
            setattr(obj, key, value)

        await self.session.commit()
        await self.session.refresh(obj)

        return obj
    
    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)
        await self.session.commit()