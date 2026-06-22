from src.offers.models import Offer
from src.offers.repository import OfferRepository


class OfferService:
    def __init__(self, repo: OfferRepository):
        self.repo = repo

    async def get_all(self, sport: str | None = None) -> list[Offer]:
        return await self.repo.get_all(sport)

    async def get_by_id(self, offer_id: int) -> Offer | None:
        return await self.repo.get_by_id(offer_id)

    async def get_by_organization(self, org_id: int) -> list[Offer]:
        return await self.repo.get_by_organization(org_id)

    async def create(self, data: dict) -> Offer:
        offer = Offer(**data)
        return await self.repo.create(offer)

    async def update(self, offer_id: int, data: dict) -> Offer | None:
        offer = await self.repo.get_by_id(offer_id)
        if not offer:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(offer, key, value)
        return await self.repo.update(offer)

    async def delete(self, offer_id: int) -> bool:
        offer = await self.repo.get_by_id(offer_id)
        if not offer:
            return False
        await self.repo.delete(offer)
        return True