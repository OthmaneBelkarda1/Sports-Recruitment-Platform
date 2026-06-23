from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.messages.schemas import MessageCreate, MessageOut
from src.messages.repository import MessageRepository
from src.messages.service import MessageService

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=MessageOut, status_code=status.HTTP_201_CREATED)
async def send_message(
    data: MessageCreate,
    db: AsyncSession = Depends(get_db),
):
    service = MessageService(MessageRepository(db), db)
    return await service.send_message(data.model_dump())


@router.get("/", response_model=list[MessageOut])
async def get_messages(
    user_id: int,
    user_role: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    service = MessageService(MessageRepository(db), db)
    return await service.get_user_messages(user_id, user_role)


@router.get("/conversation/{other_user_id}", response_model=list[MessageOut])
async def get_conversation(
    other_user_id: int,
    user_id: int,
    user_role: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    service = MessageService(MessageRepository(db), db)
    return await service.get_conversation(user_id, other_user_id, user_role)
