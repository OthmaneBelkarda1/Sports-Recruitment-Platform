from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.file_upload import save_upload, delete_upload
from src.applications.schemas import ApplicationCreate, ApplicationOut
from src.applications.repository import ApplicationRepository
from src.applications.service import ApplicationService
from src.applications.models import ApplicationStatus

router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("/", response_model=ApplicationOut, status_code=status.HTTP_201_CREATED)
async def create_application(
    data: ApplicationCreate,
    db: AsyncSession = Depends(get_db),
):
    service = ApplicationService(ApplicationRepository(db))
    application = await service.create(data.model_dump())
    return application


@router.get("/", response_model=list[ApplicationOut])
async def get_applications(
    athlete_id: int | None = None,
    offer_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    service = ApplicationService(ApplicationRepository(db))
    if athlete_id:
        return await service.get_by_athlete(athlete_id)
    if offer_id:
        return await service.get_by_offer(offer_id)
    return await service.get_all()


@router.put("/{application_id}/accept", response_model=ApplicationOut)
async def accept_application(
    application_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = ApplicationService(ApplicationRepository(db))
    application = await service.update_status(application_id, ApplicationStatus.ACCEPTED)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return application


@router.put("/{application_id}/reject", response_model=ApplicationOut)
async def reject_application(
    application_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = ApplicationService(ApplicationRepository(db))
    application = await service.update_status(application_id, ApplicationStatus.REJECTED)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return application


@router.post("/{application_id}/cv", response_model=ApplicationOut)
async def upload_cv(
    application_id: int,
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
):
    service = ApplicationService(ApplicationRepository(db))
    application = await service.get_by_id(application_id)
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    await delete_upload(application.cv)
    url = await save_upload(file, f"cv_{application_id}", cv=True)
    application = await service.upload_cv(application_id, url)
    return application
