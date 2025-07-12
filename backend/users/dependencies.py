from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies.database import get_session

from .repositories import UsersRepository
from .services import UsersService


def get_users_repository(session: AsyncSession = Depends(get_session)) -> UsersRepository:
    return UsersRepository(session)

def get_users_service(users_repository: UsersRepository = Depends(get_users_repository)) -> UsersService:
    return UsersService(users_repository)