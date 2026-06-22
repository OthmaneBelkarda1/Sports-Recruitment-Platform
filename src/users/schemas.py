from pydantic import BaseModel, EmailStr


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None


class UserOut(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True
