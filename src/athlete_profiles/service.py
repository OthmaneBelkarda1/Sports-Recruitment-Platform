from src.athlete_profiles.models import AthleteProfile
from src.athlete_profiles.repository import AthleteProfileRepository
from src.core.file_upload import delete_upload


class AthleteProfileService:
    def __init__(self, repo: AthleteProfileRepository):
        self.repo = repo

    async def get_all(self) -> list[AthleteProfile]:
        return await self.repo.get_all()

    async def get_by_id(self, profile_id: int) -> AthleteProfile | None:
        return await self.repo.get_by_id(profile_id)

    async def update(self, profile_id: int, data: dict) -> AthleteProfile | None:
        profile = await self.repo.get_by_id(profile_id)
        if not profile:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(profile, key, value)
        return await self.repo.update(profile)

    async def delete(self, profile_id: int) -> bool:
        profile = await self.repo.get_by_id(profile_id)
        if not profile:
            return False
        await delete_upload(profile.photo)
        await self.repo.delete(profile)
        return True

    async def upload_photo(self, profile_id: int, url_path: str) -> AthleteProfile:
        profile = await self.repo.get_by_id(profile_id)
        if not profile:
            raise ValueError("Profile not found")
        await delete_upload(profile.photo)
        profile.photo = url_path
        return await self.repo.update(profile)