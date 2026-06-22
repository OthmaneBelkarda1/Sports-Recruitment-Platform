from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.experiences.models import Experience


class ExperienceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, athlete_id: int | None = None) -> list[Experience]:
        query = select(Experience)
        if athlete_id is not None:
            query = query.where(Experience.athlete_id == athlete_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, experience_id: int) -> Experience | None:
        return await self.db.get(Experience, experience_id)

    async def create(self, experience: Experience) -> Experience:
        self.db.add(experience)
        await self.db.flush()
        return experience

    async def update(self, experience: Experience) -> Experience:
        await self.db.flush()
        return experience

    async def delete(self, experience: Experience) -> None:
        await self.db.delete(experience)
        await self.db.flush()
