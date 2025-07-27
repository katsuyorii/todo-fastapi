from fastapi import Request, Response

from time import time
from datetime import datetime, timezone, timedelta

from src.settings import jwt_settings
from users.repositories import UsersRepository
from core.utils.password import hashing_password, verify_password
from core.utils.jwt import create_jwt_token, verify_jwt_token
from core.repositories.redis_base import RedisBaseRepository

from .schemas import AccessTokenResponseSchema, UserRegistrationSchema, UserLoginSchema
from .exceptions import EmailAlreadyRegistered, EmailOrPasswordIncorrect, TokenMissing, TokenBlacklisted


class BlacklistTokensService:
    def __init__(self, redis_repository: RedisBaseRepository):
        self.redis_repository = redis_repository
        self.__key_prefix = 'blacklist'
    
    async def set_token_to_blacklist(self, payload: dict) -> None:
        exp = payload.get('exp')
        jti = payload.get('jti')

        current_time = int(time())
        ttl = exp - current_time

        await self.redis_repository.setex(f'{self.__key_prefix}:{jti}', 1, ttl)
    
    async def is_token_blacklisted(self, payload: dict) -> bool:
        jti = payload.get('jti')

        return await self.redis_repository.exists(f'{self.__key_prefix}:{jti}')


class JWTTokensService:
    def __init__(self, access_token_minutes_expires: int = jwt_settings.JWT_ACCESS_TOKEN_MINUTES_EXPIRES, refresh_token_days_expires: int = jwt_settings.JWT_REFRESH_TOKEN_DAYS_EXPIRES):
        self.__access_token_minutes_expires = access_token_minutes_expires
        self.__refresh_token_days_expires = refresh_token_days_expires
    
    def create_access_token(self, payload: dict) -> str:
        access_token = create_jwt_token(payload, timedelta(minutes=self.__access_token_minutes_expires))

        return access_token
    
    def create_refresh_token(self, payload: dict) -> str:
        refresh_token = create_jwt_token(payload, timedelta(days=self.__refresh_token_days_expires))

        return refresh_token
    
    def set_refresh_token_to_cookies(self, value: str, response: Response) -> None:
        response.set_cookie(
            key='refresh_token',
            value=value,
            expires=datetime.now(timezone.utc) + timedelta(days=self.__refresh_token_days_expires),
            secure=True,
            httponly=True,
            samesite='strict',
        )


class AuthService:
    def __init__(self, users_repository: UsersRepository, jwt_tokens_service: JWTTokensService, blacklist_tokens_service: BlacklistTokensService):
        self.users_repository = users_repository
        self.jwt_tokens_service = jwt_tokens_service
        self.blacklist_tokens_service = blacklist_tokens_service
    
    async def registration(self, user_data: UserRegistrationSchema) -> dict[str, str]:
        user = await self.users_repository.get_by_email(user_data.email)

        if user is not None:
            raise EmailAlreadyRegistered()

        user_data_dict = user_data.model_dump()
        user_data_dict['password'] = hashing_password(user_data.password)

        # В будущем тут необходимо будет добавить логику с отправкой email с помощью Celery + RabbitMQ
        await self.users_repository.create(user_data_dict)

        return {'message': 'User registered successfully'}

    async def authentication(self, user_data: UserLoginSchema, response: Response) -> AccessTokenResponseSchema:
        user = await self.users_repository.get_by_email(user_data.email)

        if user is None or not verify_password(user_data.password, user.password):
            raise EmailOrPasswordIncorrect()
        
        # Необходимо сделаь проверку на активированную и не заблокированную учетную запись
        #if not user.is_active:
        #    pass

        paylaod = {'sub': str(user.id), 'role': user.role}

        access_token = self.jwt_tokens_service.create_access_token(paylaod)
        refresh_token = self.jwt_tokens_service.create_refresh_token(paylaod)

        self.jwt_tokens_service.set_refresh_token_to_cookies(refresh_token, response)

        return AccessTokenResponseSchema(access_token=access_token)

    async def logout(self, request: Request, response: Response) -> dict[str, str]:
        refresh_token = request.cookies.get('refresh_token')

        if refresh_token is None:
            raise TokenMissing()
        
        payload = verify_jwt_token(refresh_token)

        if await self.blacklist_tokens_service.is_token_blacklisted(payload):
            raise TokenBlacklisted()

        await self.blacklist_tokens_service.set_token_to_blacklist(payload)

        response.delete_cookie('refresh_token')

        return {'message': 'User successfully logged out'}
    
    async def refresh(self, request: Request, response: Response) -> AccessTokenResponseSchema:
        refresh_token = request.cookies.get('refresh_token')

        if refresh_token is None:
            raise TokenMissing()
        
        payload = verify_jwt_token(refresh_token)

        if await self.blacklist_tokens_service.is_token_blacklisted(payload):
            raise TokenBlacklisted()

        await self.blacklist_tokens_service.set_token_to_blacklist(payload)

        user = await self.users_repository.get(int(payload.get('sub')))

        new_paylaod = {'sub': str(user.id), 'role': user.role}

        access_token = self.jwt_tokens_service.create_access_token(new_paylaod)
        refresh_token = self.jwt_tokens_service.create_refresh_token(new_paylaod)

        self.jwt_tokens_service.set_refresh_token_to_cookies(refresh_token, response)

        return AccessTokenResponseSchema(access_token=access_token)