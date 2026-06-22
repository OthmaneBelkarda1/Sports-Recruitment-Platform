from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.diplomas.models import Diploma


class DiplomaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, athlete_id: int | None = None) -> list[Diploma]:
        query = select(Diploma)
        if athlete_id is not None:
            query = query.where(Diploma.athlete_id == athlete_id)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, diploma_id: int) -> Diploma | None:
        return await self.db.get(Diploma, diploma_id)

    async def create(self, diploma: Diploma) -> Diploma:
        self.db.add(diploma)
        await self.db.flush()
        return diploma

    async def update(self, diploma: Diploma) -> Diploma:
        await self.db.flush()
        return diploma

    async def delete(self, diploma: Diploma) -> None:
        await self.db.delete(diploma)
        await self.db.flush()
