from fastapi import Depends

from users.repositories import UsersRepository
from users.dependencies import get_users_repository

from .services import AuthService, JWTTokensService


def get_jwt_tokens_service() -> JWTTokensService:
    return JWTTokensService()

def get_auth_service(users_repository: UsersRepository = Depends(get_users_repository), jwt_tokens_service: JWTTokensService = Depends(get_jwt_tokens_service)) -> AuthService:
    return AuthService(users_repository, jwt_tokens_service)