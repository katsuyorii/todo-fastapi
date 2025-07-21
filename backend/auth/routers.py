from fastapi import APIRouter, Depends, status

from .services import AuthService
from .dependencies import get_auth_service
from .schemas import UserRegistrationSchema


auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

@auth_router.post('/registration', status_code=status.HTTP_201_CREATED)
async def registration_user(user_data: UserRegistrationSchema, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.registration(user_data)