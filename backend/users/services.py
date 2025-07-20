from .repositories import UsersRepository


class UsersService:
    def __init__(self, users_repository: UsersRepository):
        self.users_repository = users_repository