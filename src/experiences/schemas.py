from datetime import date
from pydantic import BaseModel


class ExperienceCreate(BaseModel):
    athlete_id: int
    position: str
    organization: str
    start_date: date
    end_date: date | None = None
    description: str | None = None


class ExperienceUpdate(BaseModel):
    position: str | None = None
    organization: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None


class ExperienceOut(BaseModel):
    id: int
    athlete_id: int
    position: str
    organization: str
    start_date: date
    end_date: date | None
    description: str | None

    class Config:
        from_attributes = True