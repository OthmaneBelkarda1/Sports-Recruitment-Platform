from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.core.file_upload import save_upload
from src.athlete_profiles.schemas import AthleteProfileUpdate, AthleteProfileOut
from src.athlete_profiles.repository import AthleteProfileRepository
from src.athlete_profiles.service import AthleteProfileService

router = APIRouter(prefix="/athletes", tags=["athletes"])


@router.get("/", response_model=list[AthleteProfileOut])
async def get_profiles(db: AsyncSession = Depends(get_db)):
    service = AthleteProfileService(AthleteProfileRepository(db))
    return await service.get_all()


@router.get("/{profile_id}", response_model=AthleteProfileOut)
async def get_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    service = AthleteProfileService(AthleteProfileRepository(db))
    profile = await service.get_by_id(profile_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.put("/{profile_id}", response_model=AthleteProfileOut)
async def update_profile(
    profile_id: int,
    data: AthleteProfileUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = AthleteProfileService(AthleteProfileRepository(db))
    profile = await service.update(profile_id, data.model_dump(exclude_none=True))
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(profile_id: int, db: AsyncSession = Depends(get_db)):
    service = AthleteProfileService(AthleteProfileRepository(db))
    deleted = await service.delete(profile_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")


@router.post("/{profile_id}/photo", response_model=AthleteProfileOut)
async def upload_photo(
    profile_id: int,
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
):
    service = AthleteProfileService(AthleteProfileRepository(db))
    url_path = await save_upload(file, f"athlete_{profile_id}")
    profile = await service.upload_photo(profile_id, url_path)
    return profile
