from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.athlete_profiles.models import AthleteProfile


class AthleteProfileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[AthleteProfile]:
        result = await self.db.execute(select(AthleteProfile))
        return list(result.scalars().all())

    async def get_by_id(self, profile_id: int) -> AthleteProfile | None:
        return await self.db.get(AthleteProfile, profile_id)

    async def get_by_ids(self, ids: list[int]) -> dict[int, AthleteProfile]:
        result = await self.db.execute(select(AthleteProfile).where(AthleteProfile.id.in_(ids)))
        return {p.id: p for p in result.scalars().all()}

    async def create(self, profile: AthleteProfile) -> AthleteProfile:
        self.db.add(profile)
        await self.db.flush()
        return profile

    async def update(self, profile: AthleteProfile) -> AthleteProfile:
        await self.db.flush()
        return profile

    async def delete(self, profile: AthleteProfile) -> None:
        await self.db.delete(profile)
        await self.db.flush()
