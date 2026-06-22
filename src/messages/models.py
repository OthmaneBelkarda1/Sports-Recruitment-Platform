from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sender_id: Mapped[int] = mapped_column(Integer)
    sender_type: Mapped[str] = mapped_column(String(20))
    receiver_id: Mapped[int] = mapped_column(Integer)
    receiver_type: Mapped[str] = mapped_column(String(20))
    content: Mapped[str] = mapped_column(Text)
    sent_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
