from src.auth.models import User
from src.auth.repository import UserRepository
from src.auth.schemas import UserRegister
from src.core.security import hash_password, verify_password, generate_token
from src.athlete_profiles.models import AthleteProfile
from src.organizations.models import SportsOrganization


class AuthService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register(self, data: UserRegister) -> User:
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise ValueError("Email already registered")

        if data.role == "ATHLETE":
            user = AthleteProfile(
                email=data.email,
                password_hash=hash_password(data.password),
                auth_token=generate_token(),
                first_name=data.first_name or "",
                last_name=data.last_name or "",
                sport=data.sport or "",
                position=data.position or "",
                nationality=data.nationality or "",
                birth_date=data.birth_date,
                photo=data.photo,
            )
        elif data.role == "ORGANIZATION":
            user = SportsOrganization(
                email=data.email,
                password_hash=hash_password(data.password),
                auth_token=generate_token(),
                organization_name=data.organization_name or "",
                organization_type=data.organization_type or "",
                country=data.country or "",
                city=data.city or "",
                description=data.description,
                logo=data.logo,
            )
        else:
            raise ValueError("Invalid role")

        return await self.repo.create(user)

    async def login(self, email: str, password: str) -> User:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        user.auth_token = generate_token()
        await self.repo.update(user)
        return user

    async def get_current_user(self, token: str) -> User | None:
        return await self.repo.get_by_token(token)
