from fastapi import APIRouter, Depends, Request, Response, status

from .services import AuthService
from .dependencies import get_auth_service
from .schemas import AccessTokenResponseSchema, UserRegistrationSchema, UserLoginSchema


auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
)

@auth_router.post('/registration', status_code=status.HTTP_201_CREATED)
async def registration_user(user_data: UserRegistrationSchema, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.registration(user_data)

@auth_router.post('/login', response_model=AccessTokenResponseSchema)
async def login_user(user_data: UserLoginSchema, response: Response, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.authentication(user_data, response)

@auth_router.post('/logout')
async def logout_user(request: Request, response: Response, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.logout(request, response)

@auth_router.post('/refresh', response_model=AccessTokenResponseSchema)
async def refresh_user(request: Request, response: Response, auth_service: AuthService = Depends(get_auth_service)):
    return await auth_service.refresh(request, response)