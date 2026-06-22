from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.auth.models import User
from src.athlete_profiles.models import AthleteProfile
from src.organizations.models import SportsOrganization


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[User]:
        result_a = await self.db.execute(select(AthleteProfile))
        result_o = await self.db.execute(select(SportsOrganization))
        return list(result_a.scalars().all()) + list(result_o.scalars().all())

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.get(AthleteProfile, user_id)
        if result:
            return result
        return await self.db.get(SportsOrganization, user_id)

    async def update(self, user: User) -> User:
        await self.db.flush()
        return user

    async def delete(self, user: User) -> None:
        await self.db.delete(user)
        await self.db.flush()
