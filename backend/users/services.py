from .models import UserModel
from .repositories import UsersRepository


class UsersService:
    def __init__(self, users_repository: UsersRepository, current_user: UserModel):
        self.users_repository = users_repository
        self.current_user = current_user
    
    async def get_current_user(self) -> UserModel:
        return self.current_user