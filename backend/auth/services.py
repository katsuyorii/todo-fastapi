from users.repositories import UsersRepository

from .schemas import UserRegistrationSchema


class AuthService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository
    
    async def registration(self, user_data: UserRegistrationSchema) -> dict[str, str]:
        return {'message': 'OK'}