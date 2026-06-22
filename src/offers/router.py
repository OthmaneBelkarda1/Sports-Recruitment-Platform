from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.offers.schemas import OfferCreate, OfferUpdate, OfferOut
from src.offers.repository import OfferRepository
from src.offers.service import OfferService

router = APIRouter(prefix="/offers", tags=["offers"])


@router.post("/", response_model=OfferOut, status_code=status.HTTP_201_CREATED)
async def create_offer(
    data: OfferCreate,
    db: AsyncSession = Depends(get_db),
):
    service = OfferService(OfferRepository(db))
    offer = await service.create(data.model_dump())
    return offer


@router.get("/", response_model=list[OfferOut])
async def get_offers(
    sport: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    service = OfferService(OfferRepository(db))
    return await service.get_all(sport)


@router.get("/{offer_id}", response_model=OfferOut)
async def get_offer(offer_id: int, db: AsyncSession = Depends(get_db)):
    service = OfferService(OfferRepository(db))
    offer = await service.get_by_id(offer_id)
    if not offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found")
    return offer


@router.put("/{offer_id}", response_model=OfferOut)
async def update_offer(
    offer_id: int,
    data: OfferUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = OfferService(OfferRepository(db))
    offer = await service.update(offer_id, data.model_dump(exclude_none=True))
    if not offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found")
    return offer


@router.delete("/{offer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_offer(offer_id: int, db: AsyncSession = Depends(get_db)):
    service = OfferService(OfferRepository(db))
    deleted = await service.delete(offer_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Offer not found")
