import enum
from datetime import datetime, date
from sqlalchemy import String, Integer, DateTime, Date, Text, ForeignKey, func, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class OfferStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    CLOSED = "CLOSED"
    DRAFT = "DRAFT"


class Offer(Base):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("sports_organizations.id"))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    sport: Mapped[str] = mapped_column(String(100))
    contract_type: Mapped[str] = mapped_column(String(100))
    location: Mapped[str] = mapped_column(String(255))
    publication_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    expiration_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[OfferStatus] = mapped_column(SAEnum(OfferStatus), default=OfferStatus.ACTIVE)

    organization = relationship("SportsOrganization", back_populates="offers")
    applications = relationship("Application", back_populates="offer", cascade="all, delete-orphan")
