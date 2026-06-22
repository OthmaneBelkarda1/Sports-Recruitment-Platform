from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.diplomas.schemas import DiplomaCreate, DiplomaUpdate, DiplomaOut
from src.diplomas.repository import DiplomaRepository
from src.diplomas.service import DiplomaService

router = APIRouter(prefix="/diplomas", tags=["diplomas"])


@router.post("/", response_model=DiplomaOut, status_code=status.HTTP_201_CREATED)
async def create_diploma(
    data: DiplomaCreate,
    db: AsyncSession = Depends(get_db),
):
    service = DiplomaService(DiplomaRepository(db))
    diploma = await service.create(data.model_dump())
    return diploma


@router.get("/", response_model=list[DiplomaOut])
async def get_diplomas(
    athlete_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    service = DiplomaService(DiplomaRepository(db))
    return await service.get_all(athlete_id)


@router.put("/{diploma_id}", response_model=DiplomaOut)
async def update_diploma(
    diploma_id: int,
    data: DiplomaUpdate,
    db: AsyncSession = Depends(get_db),
):
    service = DiplomaService(DiplomaRepository(db))
    diploma = await service.update(diploma_id, data.model_dump(exclude_none=True))
    if not diploma:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diploma not found")
    return diploma


@router.delete("/{diploma_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diploma(diploma_id: int, db: AsyncSession = Depends(get_db)):
    service = DiplomaService(DiplomaRepository(db))
    deleted = await service.delete(diploma_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Diploma not found")
