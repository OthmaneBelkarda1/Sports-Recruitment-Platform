from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, union

from src.auth.models import User
from src.athlete_profiles.models import AthleteProfile
from src.organizations.models import SportsOrganization


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(AthleteProfile).where(AthleteProfile.email == email)
        )
        user = result.scalar_one_or_none()
        if user:
            return user
        result = await self.db.execute(
            select(SportsOrganization).where(SportsOrganization.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_token(self, token: str) -> User | None:
        result = await self.db.execute(
            select(AthleteProfile).where(AthleteProfile.auth_token == token)
        )
        user = result.scalar_one_or_none()
        if user:
            return user
        result = await self.db.execute(
            select(SportsOrganization).where(SportsOrganization.auth_token == token)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.db.get(AthleteProfile, user_id)
        if result:
            return result
        return await self.db.get(SportsOrganization, user_id)

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        return user

    async def update(self, user: User) -> User:
        await self.db.flush()
        return user
