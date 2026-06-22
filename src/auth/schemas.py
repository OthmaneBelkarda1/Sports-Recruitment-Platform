from datetime import date
from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: str = "ATHLETE"
    first_name: str | None = None
    last_name: str | None = None
    sport: str | None = None
    position: str | None = None
    nationality: str | None = None
    birth_date: date | None = None
    photo: str | None = None
    organization_name: str | None = None
    organization_type: str | None = None
    country: str | None = None
    city: str | None = None
    description: str | None = None
    logo: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    id: int
    email: str
    role: str
    token: str


class UserOut(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True
