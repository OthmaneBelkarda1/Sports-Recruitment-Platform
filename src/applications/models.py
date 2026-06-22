import enum
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, Text, ForeignKey, func, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class ApplicationStatus(str, enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    athlete_id: Mapped[int] = mapped_column(ForeignKey("athlete_profiles.id"))
    offer_id: Mapped[int] = mapped_column(ForeignKey("offers.id"))
    application_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    status: Mapped[ApplicationStatus] = mapped_column(
        SAEnum(ApplicationStatus), default=ApplicationStatus.PENDING
    )
    cv: Mapped[str | None] = mapped_column(Text, nullable=True)
    motivation_letter: Mapped[str | None] = mapped_column(Text, nullable=True)

    athlete = relationship("AthleteProfile", back_populates="applications")
    offer = relationship("Offer", back_populates="applications")
