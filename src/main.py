from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from storage3.types import CreateOrUpdateBucketOptions

from src.core.database import get_engine, Base
from src.core.config import settings
from src.core.migrate import migrate_schema
from src.auth.router import router as auth_router
from src.users.router import router as users_router
from src.athlete_profiles.router import router as athlete_profiles_router
from src.organizations.router import router as organizations_router
from src.diplomas.router import router as diplomas_router
from src.experiences.router import router as experiences_router
from src.offers.router import router as offers_router
from src.applications.router import router as applications_router
from src.messages.router import router as messages_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
    try:
        supabase.storage.create_bucket(
            settings.SUPABASE_STORAGE_BUCKET,
            options=CreateOrUpdateBucketOptions(public=True),
        )
    except Exception:
        pass  # bucket already exists
    async with get_engine().begin() as conn:
        await migrate_schema(conn)
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="Sports Recruitment Platform",
    description="API for connecting athletes with sports organizations",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(athlete_profiles_router)
app.include_router(organizations_router)
app.include_router(diplomas_router)
app.include_router(experiences_router)
app.include_router(offers_router)
app.include_router(applications_router)
app.include_router(messages_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
