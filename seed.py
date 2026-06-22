"""Seed script to populate the database with sample data.

Usage:
    python seed.py
"""
import asyncio
from datetime import date

from src.core.database import get_session_factory, get_engine, Base
from src.core.security import hash_password
from src.athlete_profiles.models import AthleteProfile
from src.organizations.models import SportsOrganization
from src.diplomas.models import Diploma
from src.experiences.models import Experience
from src.offers.models import Offer, OfferStatus
from src.applications.models import Application, ApplicationStatus
from src.messages.models import Message


async def seed():
    async with get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with get_session_factory()() as session:
        athlete1 = AthleteProfile(
            email="athlete1@example.com",
            password_hash=hash_password("password123"),
            auth_token=None,
            first_name="Lionel",
            last_name="Messi",
            sport="Football",
            position="Forward",
            nationality="Argentina",
            birth_date=date(1987, 6, 24),
        )
        athlete2 = AthleteProfile(
            email="athlete2@example.com",
            password_hash=hash_password("password123"),
            auth_token=None,
            first_name="LeBron",
            last_name="James",
            sport="Basketball",
            position="Forward",
            nationality="USA",
            birth_date=date(1984, 12, 30),
        )
        org1 = SportsOrganization(
            email="org1@example.com",
            password_hash=hash_password("password123"),
            auth_token=None,
            organization_name="FC Barcelona",
            organization_type="Professional Club",
            country="Spain",
            city="Barcelona",
            description="One of the most famous football clubs in the world.",
        )
        org2 = SportsOrganization(
            email="org2@example.com",
            password_hash=hash_password("password123"),
            auth_token=None,
            organization_name="LA Lakers",
            organization_type="Professional Club",
            country="USA",
            city="Los Angeles",
            description="NBA basketball team.",
        )
        session.add_all([athlete1, athlete2, org1, org2])
        await session.flush()

        diploma1 = Diploma(
            athlete_id=athlete1.id,
            title="UEFA Pro License",
            institution="UEFA",
            year=2020,
            is_certification=True,
        )
        diploma2 = Diploma(
            athlete_id=athlete2.id,
            title="Basketball Coaching Certificate",
            institution="NBA Academy",
            year=2021,
            is_certification=True,
        )
        session.add_all([diploma1, diploma2])
        await session.flush()

        exp1 = Experience(
            athlete_id=athlete1.id,
            position="Forward",
            organization="Paris Saint-Germain",
            start_date=date(2021, 8, 1),
            end_date=date(2023, 6, 30),
            description="Played as forward for PSG.",
        )
        exp2 = Experience(
            athlete_id=athlete2.id,
            position="Forward",
            organization="Cleveland Cavaliers",
            start_date=date(2003, 10, 1),
            end_date=date(2010, 6, 30),
            description="Started NBA career with Cavaliers.",
        )
        session.add_all([exp1, exp2])
        await session.flush()

        offer1 = Offer(
            organization_id=org1.id,
            title="Football Player Wanted",
            description="Looking for a skilled forward.",
            sport="Football",
            contract_type="Full-time",
            location="Barcelona, Spain",
            expiration_date=date(2025, 12, 31),
            status=OfferStatus.ACTIVE,
        )
        offer2 = Offer(
            organization_id=org2.id,
            title="Basketball Player Scout",
            description="Seeking experienced basketball scout.",
            sport="Basketball",
            contract_type="Part-time",
            location="Los Angeles, USA",
            expiration_date=date(2025, 11, 30),
            status=OfferStatus.ACTIVE,
        )
        session.add_all([offer1, offer2])
        await session.flush()

        app1 = Application(
            athlete_id=athlete1.id,
            offer_id=offer2.id,
            status=ApplicationStatus.PENDING,
            cv="Experienced football player looking to transition.",
            motivation_letter="I am interested in scouting.",
        )
        app2 = Application(
            athlete_id=athlete2.id,
            offer_id=offer1.id,
            status=ApplicationStatus.PENDING,
            cv="NBA star with leadership skills.",
            motivation_letter="I want to play football!",
        )
        session.add_all([app1, app2])
        await session.flush()

        msg1 = Message(
            sender_id=athlete1.id,
            sender_type="athlete",
            receiver_id=org1.id,
            receiver_type="organization",
            content="Hello, I am interested in your offer.",
        )
        msg2 = Message(
            sender_id=org1.id,
            sender_type="organization",
            receiver_id=athlete1.id,
            receiver_type="athlete",
            content="Great! Please apply through the platform.",
        )
        session.add_all([msg1, msg2])
        await session.flush()

        await session.commit()

    print("Database seeded successfully!")


if __name__ == "__main__":
    asyncio.run(seed())
