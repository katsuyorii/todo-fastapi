from fastapi import APIRouter, Depends

from .dependencies import get_users_service
from .services import UsersService
from .schemas import UserResponseSchema, UserUpdateSchema


users_router = APIRouter(
    prefix='/users',
    tags=['Users'],
)

@users_router.get('/me', response_model=UserResponseSchema)
async def get_me(users_service: UsersService = Depends(get_users_service)):
    return await users_service.get_current_user()

@users_router.patch('/me', response_model=UserResponseSchema)
async def update_me(updated_user_data: UserUpdateSchema, users_service: UsersService = Depends(get_users_service)):
    return await users_service.update_current_user(updated_user_data)