from datetime import datetime, date
from pydantic import BaseModel


class OfferCreate(BaseModel):
    organization_id: int
    title: str
    description: str
    sport: str
    contract_type: str
    location: str
    expiration_date: date | None = None


class OfferUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    sport: str | None = None
    contract_type: str | None = None
    location: str | None = None
    expiration_date: date | None = None
    status: str | None = None


class OfferOut(BaseModel):
    id: int
    organization_id: int
    title: str
    description: str
    sport: str
    contract_type: str
    location: str
    publication_date: datetime
    expiration_date: date | None
    status: str

    class Config:
        from_attributes = True