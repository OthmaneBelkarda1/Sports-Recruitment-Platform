from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.offers.models import Offer


class OfferRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, sport: str | None = None) -> list[Offer]:
        query = select(Offer)
        if sport:
            query = query.where(Offer.sport == sport)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def get_by_id(self, offer_id: int) -> Offer | None:
        return await self.db.get(Offer, offer_id)

    async def get_by_organization(self, org_id: int) -> list[Offer]:
        result = await self.db.execute(
            select(Offer).where(Offer.organization_id == org_id)
        )
        return list(result.scalars().all())

    async def create(self, offer: Offer) -> Offer:
        self.db.add(offer)
        await self.db.flush()
        return offer

    async def update(self, offer: Offer) -> Offer:
        await self.db.flush()
        return offer

    async def delete(self, offer: Offer) -> None:
        await self.db.delete(offer)
        await self.db.flush()
