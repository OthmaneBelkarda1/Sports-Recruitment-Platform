from pydantic import BaseModel


class DiplomaCreate(BaseModel):
    athlete_id: int
    title: str
    institution: str
    year: int
    is_certification: bool = False


class DiplomaUpdate(BaseModel):
    title: str | None = None
    institution: str | None = None
    year: int | None = None
    is_certification: bool | None = None


class DiplomaOut(BaseModel):
    id: int
    athlete_id: int
    title: str
    institution: str
    year: int
    is_certification: bool

    class Config:
        from_attributes = True