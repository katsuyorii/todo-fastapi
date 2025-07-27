from fastapi import APIRouter, Depends

from .dependencies import get_users_service
from .services import UsersService
from .schemas import UserResponseSchema


users_router = APIRouter(
    prefix='/users',
    tags=['Users'],
)

@users_router.get('/me', response_model=UserResponseSchema)
async def get_me(users_service: UsersService = Depends(get_users_service)):
    return await users_service.get_current_user()