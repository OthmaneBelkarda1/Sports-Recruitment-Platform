from sqlalchemy import String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base


class Diploma(Base):
    __tablename__ = "diplomas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    athlete_id: Mapped[int] = mapped_column(ForeignKey("athlete_profiles.id"))
    title: Mapped[str] = mapped_column(String(255))
    institution: Mapped[str] = mapped_column(String(255))
    year: Mapped[int] = mapped_column(Integer)
    is_certification: Mapped[bool] = mapped_column(Boolean, default=False)

    athlete = relationship("AthleteProfile", back_populates="diplomas")
