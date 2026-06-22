from src.organizations.models import SportsOrganization
from src.organizations.repository import OrganizationRepository
from src.core.file_upload import delete_upload


class OrganizationService:
    def __init__(self, repo: OrganizationRepository):
        self.repo = repo

    async def get_all(self) -> list[SportsOrganization]:
        return await self.repo.get_all()

    async def get_by_id(self, org_id: int) -> SportsOrganization | None:
        return await self.repo.get_by_id(org_id)

    async def update(self, org_id: int, data: dict) -> SportsOrganization | None:
        org = await self.repo.get_by_id(org_id)
        if not org:
            return None
        for key, value in data.items():
            if value is not None:
                setattr(org, key, value)
        return await self.repo.update(org)

    async def delete(self, org_id: int) -> bool:
        org = await self.repo.get_by_id(org_id)
        if not org:
            return False
        await delete_upload(org.logo)
        await self.repo.delete(org)
        return True

    async def upload_logo(self, org_id: int, url_path: str) -> SportsOrganization:
        org = await self.repo.get_by_id(org_id)
        if not org:
            raise ValueError("Organization not found")
        await delete_upload(org.logo)
        org.logo = url_path
        return await self.repo.update(org)