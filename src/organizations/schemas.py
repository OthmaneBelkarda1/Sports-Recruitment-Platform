from pydantic import BaseModel


class OrganizationCreate(BaseModel):
    organization_name: str
    organization_type: str
    country: str
    city: str
    description: str | None = None
    logo: str | None = None


class OrganizationUpdate(BaseModel):
    organization_name: str | None = None
    organization_type: str | None = None
    country: str | None = None
    city: str | None = None
    description: str | None = None
    logo: str | None = None


class OrganizationOut(BaseModel):
    id: int
    email: str
    is_active: bool
    organization_name: str
    organization_type: str
    country: str
    city: str
    description: str | None
    logo: str | None

    class Config:
        from_attributes = True
