from datetime import date
from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.auth.models import User


class AthleteProfile(User):
    __tablename__ = "athlete_profiles"
    _role = "ATHLETE"

    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    sport: Mapped[str] = mapped_column(String(100))
    position: Mapped[str] = mapped_column(String(100))
    nationality: Mapped[str] = mapped_column(String(100))
    birth_date: Mapped[date] = mapped_column(Date)
    photo: Mapped[str | None] = mapped_column(String(500), nullable=True)

    diplomas = relationship("Diploma", back_populates="athlete", cascade="all, delete-orphan")
    experiences = relationship("Experience", back_populates="athlete", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="athlete", cascade="all, delete-orphan")
