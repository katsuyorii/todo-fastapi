from fastapi import Depends

from users.repositories import UsersRepository
from users.dependencies import get_users_repository
from core.dependencies.redis import get_redis_repository

from .services import AuthService, JWTTokensService, BlacklistTokensService


def get_blacklist_tokens_service(redis_repository = Depends(get_redis_repository)) -> BlacklistTokensService:
    return BlacklistTokensService(redis_repository)

def get_jwt_tokens_service() -> JWTTokensService:
    return JWTTokensService()

def get_auth_service(users_repository: UsersRepository = Depends(get_users_repository), jwt_tokens_service: JWTTokensService = Depends(get_jwt_tokens_service), blacklist_tokens_service: BlacklistTokensService = Depends(get_blacklist_tokens_service)) -> AuthService:
    return AuthService(users_repository, jwt_tokens_service, blacklist_tokens_service)