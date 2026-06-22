from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.auth.models import User


class SportsOrganization(User):
    __tablename__ = "sports_organizations"
    _role = "ORGANIZATION"

    organization_name: Mapped[str] = mapped_column(String(200))
    organization_type: Mapped[str] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    logo: Mapped[str | None] = mapped_column(String(500), nullable=True)

    offers = relationship("Offer", back_populates="organization", cascade="all, delete-orphan")
