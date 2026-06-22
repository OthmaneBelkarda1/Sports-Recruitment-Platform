from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.organizations.models import SportsOrganization


class OrganizationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[SportsOrganization]:
        result = await self.db.execute(select(SportsOrganization))
        return list(result.scalars().all())

    async def get_by_id(self, org_id: int) -> SportsOrganization | None:
        return await self.db.get(SportsOrganization, org_id)

    async def get_by_ids(self, ids: list[int]) -> dict[int, SportsOrganization]:
        result = await self.db.execute(
            select(SportsOrganization).where(SportsOrganization.id.in_(ids))
        )
        return {o.id: o for o in result.scalars().all()}

    async def create(self, org: SportsOrganization) -> SportsOrganization:
        self.db.add(org)
        await self.db.flush()
        return org

    async def update(self, org: SportsOrganization) -> SportsOrganization:
        await self.db.flush()
        return org

    async def delete(self, org: SportsOrganization) -> None:
        await self.db.delete(org)
        await self.db.flush()
