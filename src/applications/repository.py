from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.applications.models import Application


class ApplicationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Application]:
        result = await self.db.execute(select(Application))
        return list(result.scalars().all())

    async def get_by_id(self, application_id: int) -> Application | None:
        return await self.db.get(Application, application_id)

    async def get_by_athlete(self, athlete_id: int) -> list[Application]:
        result = await self.db.execute(
            select(Application).where(Application.athlete_id == athlete_id)
        )
        return list(result.scalars().all())

    async def get_by_offer(self, offer_id: int) -> list[Application]:
        result = await self.db.execute(
            select(Application).where(Application.offer_id == offer_id)
        )
        return list(result.scalars().all())

    async def create(self, application: Application) -> Application:
        self.db.add(application)
        await self.db.flush()
        return application

    async def update(self, application: Application) -> Application:
        await self.db.flush()
        return application
