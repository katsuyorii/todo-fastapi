from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.repositories.database_base import DatabaseBaseRepository

from .models import UserModel


class UsersRepository(DatabaseBaseRepository):
    def __init__(self, session: AsyncSession, model: UserModel = UserModel):
        super().__init__(session, model)
    
    async def get_by_email(self, email: str) -> UserModel | None:
        user = await self.session.execute(select(UserModel).where(UserModel.email == email))

        return user.scalar_one_or_none()