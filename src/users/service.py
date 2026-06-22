from src.auth.models import User
from src.users.repository import UserRepository
from src.core.security import hash_password


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_all_users(self) -> list[User]:
        return await self.repo.get_all()

    async def get_user(self, user_id: int) -> User | None:
        return await self.repo.get_by_id(user_id)

    async def update_user(self, user_id: int, data: dict) -> User | None:
        user = await self.repo.get_by_id(user_id)
        if not user:
            return None
        if "email" in data:
            user.email = data["email"]
        if "password" in data:
            user.password_hash = hash_password(data["password"])
        return await self.repo.update(user)

    async def delete_user(self, user_id: int) -> bool:
        user = await self.repo.get_by_id(user_id)
        if not user:
            return False
        await self.repo.delete(user)
        return True
