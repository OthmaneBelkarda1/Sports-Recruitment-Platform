from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_db
from src.auth.schemas import UserRegister, UserLogin, AuthResponse
from src.auth.repository import UserRepository
from src.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    service = AuthService(UserRepository(db))
    try:
        user = await service.register(data)
        return AuthResponse(
            id=user.id, email=user.email, role=user.role, token=user.auth_token
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=AuthResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    service = AuthService(UserRepository(db))
    try:
        user = await service.login(data.email, data.password)
        return AuthResponse(
            id=user.id, email=user.email, role=user.role, token=user.auth_token
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
