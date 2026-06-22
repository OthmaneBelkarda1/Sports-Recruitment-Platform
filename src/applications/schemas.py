from datetime import datetime
from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    athlete_id: int
    offer_id: int
    motivation_letter: str | None = None


class ApplicationOut(BaseModel):
    id: int
    athlete_id: int
    offer_id: int
    application_date: datetime
    status: str
    cv: str | None
    motivation_letter: str | None

    class Config:
        from_attributes = True