from src.experiences.models import Experience
from src.experiences.repository import ExperienceRepository


class ExperienceService:
    def __init__(self, repo: ExperienceRepository):
        self.repo = repo

    async def get_all(self, athlete_id: int | None = None) -> list[Experience]:
        return await self.repo.get_all(athlete_id)

    async def get_by_id(self, experience_id: int) -> Experience | None:
        return await self.repo.get_by_id(experience_id)

    async def create(self, data: dict) -> Experience:
        experience = Experience(**data)
        return await self.repo.create(experience)

    async def update(self, experience_id: int, data: dict) -> Experience | None:
        experience = await self.repo.get_by_id(experience_id)
        if not experience:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(experience, key, value)
        return await self.repo.update(experience)

    async def delete(self, experience_id: int) -> bool:
        experience = await self.repo.get_by_id(experience_id)
        if not experience:
            return False
        await self.repo.delete(experience)
        return True