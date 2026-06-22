from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.experiences.schemas import ExperienceCreate, ExperienceUpdate, ExperienceOut
from src.experiences.repository import ExperienceRepository
from src.experiences.service import ExperienceService

router = APIRouter(prefix="/experiences", tags=["experiences"])


@router.post("/", response_model=ExperienceOut, status_code=status.HTTP_201_CREATED)
async def create_experience(
    data: ExperienceCreate,
    db: AsyncSession = Depends(get_db),
):
    service = ExperienceService(ExperienceRepository(db))
    experience = await service.create(data.model_dump())
    return experience


@router.get("/", response_model=list[ExperienceOut])
async def get_experiences(
    athlete_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    service = ExperienceService(ExperienceRepository(db))
    return await service.get_all(athlete_id)


@router.put("/{experience_id}", response_model=ExperienceOut)
async def update_experience(
    experience_id: int,
    data: ExperienceUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = ExperienceService(ExperienceRepository(db))
    experience = await service.update(experience_id, data.model_dump(exclude_none=True))
    if not experience:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")
    return experience


@router.delete("/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_experience(experience_id: int, db: AsyncSession = Depends(get_db)):
    service = ExperienceService(ExperienceRepository(db))
    deleted = await service.delete(experience_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")
