from fastapi import Response

from datetime import datetime, timedelta

from src.settings import jwt_settings
from users.repositories import UsersRepository
from core.utils.password import hashing_password
from core.utils.jwt import create_jwt_token

from .schemas import UserRegistrationSchema
from .exceptions import EmailAlreadyRegistered


class JWTTokensService:
    def __init__(self, access_token_minutes_expires: int = jwt_settings.JWT_ACCESS_TOKEN_MINUTES_EXPIRES, refresh_token_days_expires: int = jwt_settings.JWT_REFRESH_TOKEN_DAYS_EXPIRES):
        self.access_token_minutes_expires = access_token_minutes_expires
        self.refresh_token_days_expires = refresh_token_days_expires
    
    def create_access_token(self, payload: dict) -> str:
        access_token = create_jwt_token(payload, timedelta(minutes=self.access_token_minutes_expires))

        return access_token
    
    def create_refresh_token(self, payload: dict) -> str:
        refresh_token = create_jwt_token(payload, timedelta(days=self.refresh_token_days_expires))

        return refresh_token
    
    def set_token_to_cookies(self, key: str, value: str, exp: float, httponly: bool, response: Response) -> None:
        response.set_cookie(
            key=key,
            value=value,
            expires=datetime.fromtimestamp(exp),
            secure=True,
            httponly=httponly,
            samesite='strict',
        )


class AuthService:
    def __init__(self, users_repository: UsersRepository, jwt_tokens_service: JWTTokensService):
        self.users_repository = users_repository
        self.jwt_tokens_service = jwt_tokens_service
    
    async def registration(self, user_data: UserRegistrationSchema) -> dict[str, str]:
        user = await self.users_repository.get_by_email(user_data.email)

        if user is not None:
            raise EmailAlreadyRegistered()

        user_data_dict = user_data.model_dump()
        user_data_dict['password'] = hashing_password(user_data.password)

        # В будущем тут необходимо будет добавить логику с отправкой email с помощью Celery + RabbitMQ
        await self.users_repository.create(user_data_dict)

        return {'message': 'User registered successfully'}