from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from src.messages.models import Message


class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_messages(self, user_id: int) -> list[Message]:
        result = await self.db.execute(
            select(Message)
            .where(or_(Message.sender_id == user_id, Message.receiver_id == user_id))
            .order_by(Message.sent_date.desc())
        )
        return list(result.scalars().all())

    async def get_conversation(self, user1_id: int, user2_id: int) -> list[Message]:
        result = await self.db.execute(
            select(Message)
            .where(
                or_(
                    (Message.sender_id == user1_id) & (Message.receiver_id == user2_id),
                    (Message.sender_id == user2_id) & (Message.receiver_id == user1_id),
                )
            )
            .order_by(Message.sent_date.asc())
        )
        return list(result.scalars().all())

    async def create(self, message: Message) -> Message:
        self.db.add(message)
        await self.db.flush()
        return message
