from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.file_upload import save_upload
from src.organizations.schemas import OrganizationUpdate, OrganizationOut
from src.organizations.repository import OrganizationRepository
from src.organizations.service import OrganizationService

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.get("/", response_model=list[OrganizationOut])
async def get_organizations(db: AsyncSession = Depends(get_db)):
    service = OrganizationService(OrganizationRepository(db))
    return await service.get_all()


@router.get("/{org_id}", response_model=OrganizationOut)
async def get_organization(org_id: int, db: AsyncSession = Depends(get_db)):
    service = OrganizationService(OrganizationRepository(db))
    org = await service.get_by_id(org_id)
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return org


@router.put("/{org_id}", response_model=OrganizationOut)
async def update_organization(
    org_id: int,
    data: OrganizationUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = OrganizationService(OrganizationRepository(db))
    org = await service.update(org_id, data.model_dump(exclude_none=True))
    if not org:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
    return org


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(org_id: int, db: AsyncSession = Depends(get_db)):
    service = OrganizationService(OrganizationRepository(db))
    deleted = await service.delete(org_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")


@router.post("/{org_id}/logo", response_model=OrganizationOut)
async def upload_logo(
    org_id: int,
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
):
    service = OrganizationService(OrganizationRepository(db))
    url_path = await save_upload(file, f"org_{org_id}")
    org = await service.upload_logo(org_id, url_path)
    return org
