from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies.database import get_session
from core.utils.jwt import verify_jwt_token

from .models import UserModel
from .repositories import UsersRepository
from .services import UsersService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_users_repository(session: AsyncSession = Depends(get_session)) -> UsersRepository:
    return UsersRepository(session)

async def get_current_user(token: str = Depends(oauth2_scheme), users_repository: UsersRepository = Depends(get_users_repository)) -> UserModel:
    payload = verify_jwt_token(token)

    current_user = await users_repository.get(int(payload.get('sub')))

    return current_user

def get_users_service(users_repository: UsersRepository = Depends(get_users_repository), current_user: UserModel = Depends(get_current_user)) -> UsersService:
    return UsersService(users_repository, current_user)