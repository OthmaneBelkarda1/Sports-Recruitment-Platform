from sqlalchemy.ext.asyncio import AsyncSession

from src.athlete_profiles.repository import AthleteProfileRepository
from src.messages.models import Message
from src.messages.repository import MessageRepository
from src.messages.schemas import MessageOut, ParticipantInfo
from src.organizations.repository import OrganizationRepository


class MessageService:
    def __init__(self, repo: MessageRepository, db: AsyncSession):
        self.repo = repo
        self._athlete_repo = AthleteProfileRepository(db)
        self._org_repo = OrganizationRepository(db)

    async def _resolve_role(self, user_id: int) -> str | None:
        athlete = await self._athlete_repo.get_by_id(user_id)
        if athlete:
            return "athlete"
        org = await self._org_repo.get_by_id(user_id)
        if org:
            return "organization"
        return None

    async def _resolve_participant(self, participant_id: int, participant_type: str) -> ParticipantInfo:
        if participant_type == "athlete":
            profile = await self._athlete_repo.get_by_id(participant_id)
            if not profile:
                return ParticipantInfo(id=participant_id, type="athlete", email="", name="[deleted]")
            return ParticipantInfo(
                id=profile.id,
                type="athlete",
                email=profile.email,
                name=f"{profile.first_name} {profile.last_name}",
                photo=profile.photo,
            )
        org = await self._org_repo.get_by_id(participant_id)
        if not org:
            return ParticipantInfo(id=participant_id, type="organization", email="", name="[deleted]")
        return ParticipantInfo(
            id=org.id,
            type="organization",
            email=org.email,
            name=org.organization_name,
            photo=org.logo,
        )

    async def _to_out(self, message: Message, user_id: int, user_role: str) -> MessageOut:
        sender = await self._resolve_participant(message.sender_id, message.sender_type)
        receiver = await self._resolve_participant(message.receiver_id, message.receiver_type)

        is_sender = user_id == message.sender_id and user_role == message.sender_type
        return MessageOut(
            id=message.id,
            direction="sent" if is_sender else "received",
            other=receiver if is_sender else sender,
            content=message.content,
            sent_date=message.sent_date,
        )

    async def get_user_messages(self, user_id: int, user_role: str | None = None) -> list[MessageOut]:
        if user_role is None:
            user_role = await self._resolve_role(user_id)
        messages = await self.repo.get_user_messages(user_id)
        return [await self._to_out(m, user_id, user_role) for m in messages]

    async def get_conversation(self, user1_id: int, user2_id: int, user_role: str | None = None) -> list[MessageOut]:
        if user_role is None:
            user_role = await self._resolve_role(user1_id)
        messages = await self.repo.get_conversation(user1_id, user2_id)
        return [await self._to_out(m, user1_id, user_role) for m in messages]

    async def send_message(self, data: dict) -> MessageOut:
        message = Message(**data)
        created = await self.repo.create(message)
        return await self._to_out(created, data["sender_id"], data["sender_type"])
