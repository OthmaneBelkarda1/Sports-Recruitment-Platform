from src.applications.models import Application, ApplicationStatus
from src.applications.repository import ApplicationRepository


class ApplicationService:
    def __init__(self, repo: ApplicationRepository):
        self.repo = repo

    async def get_all(self) -> list[Application]:
        return await self.repo.get_all()

    async def get_by_id(self, application_id: int) -> Application | None:
        return await self.repo.get_by_id(application_id)

    async def get_by_athlete(self, athlete_id: int) -> list[Application]:
        return await self.repo.get_by_athlete(athlete_id)

    async def get_by_offer(self, offer_id: int) -> list[Application]:
        return await self.repo.get_by_offer(offer_id)

    async def create(self, data: dict) -> Application:
        application = Application(**data)
        return await self.repo.create(application)

    async def update_status(
        self, application_id: int, status: ApplicationStatus
    ) -> Application | None:
        application = await self.repo.get_by_id(application_id)
        if not application:
            return None
        application.status = status
        return await self.repo.update(application)

    async def upload_cv(self, application_id: int, url: str) -> Application:
        application = await self.repo.get_by_id(application_id)
        if not application:
            raise ValueError("Application not found")
        application.cv = url
        return await self.repo.update(application)
