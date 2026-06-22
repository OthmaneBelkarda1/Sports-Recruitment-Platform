from datetime import date
from pydantic import BaseModel


class AthleteProfileCreate(BaseModel):
    first_name: str
    last_name: str
    sport: str
    position: str
    nationality: str
    birth_date: date
    photo: str | None = None


class AthleteProfileUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    sport: str | None = None
    position: str | None = None
    nationality: str | None = None
    birth_date: date | None = None
    photo: str | None = None


class AthleteProfileOut(BaseModel):
    id: int
    email: str
    is_active: bool
    first_name: str
    last_name: str
    sport: str
    position: str
    nationality: str
    birth_date: date
    photo: str | None

    class Config:
        from_attributes = True
