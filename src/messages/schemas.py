from datetime import datetime
from pydantic import BaseModel


class MessageCreate(BaseModel):
    sender_id: int
    sender_type: str
    receiver_id: int
    receiver_type: str
    content: str


class ParticipantInfo(BaseModel):
    id: int
    type: str
    email: str
    name: str
    photo: str | None = None


class MessageOut(BaseModel):
    id: int
    direction: str  # "sent" or "received"
    other: ParticipantInfo
    content: str
    sent_date: datetime