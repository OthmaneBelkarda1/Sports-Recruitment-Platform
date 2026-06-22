from src.diplomas.models import Diploma
from src.diplomas.repository import DiplomaRepository


class DiplomaService:
    def __init__(self, repo: DiplomaRepository):
        self.repo = repo

    async def get_all(self, athlete_id: int | None = None) -> list[Diploma]:
        return await self.repo.get_all(athlete_id)

    async def get_by_id(self, diploma_id: int) -> Diploma | None:
        return await self.repo.get_by_id(diploma_id)

    async def create(self, data: dict) -> Diploma:
        diploma = Diploma(**data)
        return await self.repo.create(diploma)

    async def update(self, diploma_id: int, data: dict) -> Diploma | None:
        diploma = await self.repo.get_by_id(diploma_id)
        if not diploma:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(diploma, key, value)
        return await self.repo.update(diploma)

    async def delete(self, diploma_id: int) -> bool:
        diploma = await self.repo.get_by_id(diploma_id)
        if not diploma:
            return False
        await self.repo.delete(diploma)
        return True