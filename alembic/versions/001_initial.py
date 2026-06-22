"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-06-18
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "athlete_profiles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("auth_token", sa.String(255), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=False),
        sa.Column("sport", sa.String(100), nullable=False),
        sa.Column("position", sa.String(100), nullable=False),
        sa.Column("nationality", sa.String(100), nullable=False),
        sa.Column("birth_date", sa.Date(), nullable=False),
        sa.Column("photo", sa.String(500), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_athlete_profiles_id"), "athlete_profiles", ["id"])
    op.create_index(op.f("ix_athlete_profiles_email"), "athlete_profiles", ["email"], unique=True)

    op.create_table(
        "sports_organizations",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("auth_token", sa.String(255), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("organization_name", sa.String(200), nullable=False),
        sa.Column("organization_type", sa.String(100), nullable=False),
        sa.Column("country", sa.String(100), nullable=False),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("description", sa.String(2000), nullable=True),
        sa.Column("logo", sa.String(500), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sports_organizations_id"), "sports_organizations", ["id"])
    op.create_index(
        op.f("ix_sports_organizations_email"), "sports_organizations", ["email"], unique=True
    )

    op.create_table(
        "diplomas",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("athlete_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("institution", sa.String(255), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("is_certification", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.ForeignKeyConstraint(["athlete_id"], ["athlete_profiles.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_diplomas_id"), "diplomas", ["id"])

    op.create_table(
        "experiences",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("athlete_id", sa.Integer(), nullable=False),
        sa.Column("position", sa.String(255), nullable=False),
        sa.Column("organization", sa.String(255), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["athlete_id"], ["athlete_profiles.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_experiences_id"), "experiences", ["id"])

    op.create_table(
        "offers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("sport", sa.String(100), nullable=False),
        sa.Column("contract_type", sa.String(100), nullable=False),
        sa.Column("location", sa.String(255), nullable=False),
        sa.Column(
            "publication_date",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("expiration_date", sa.Date(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("ACTIVE", "CLOSED", "DRAFT", name="offerstatus"),
            nullable=False,
            server_default="ACTIVE",
        ),
        sa.ForeignKeyConstraint(["organization_id"], ["sports_organizations.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_offers_id"), "offers", ["id"])

    op.create_table(
        "applications",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("athlete_id", sa.Integer(), nullable=False),
        sa.Column("offer_id", sa.Integer(), nullable=False),
        sa.Column(
            "application_date",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum("PENDING", "ACCEPTED", "REJECTED", name="applicationstatus"),
            nullable=False,
            server_default="PENDING",
        ),
        sa.Column("cv", sa.Text(), nullable=True),
        sa.Column("motivation_letter", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["athlete_id"], ["athlete_profiles.id"],),
        sa.ForeignKeyConstraint(["offer_id"], ["offers.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_applications_id"), "applications", ["id"])

    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("sender_id", sa.Integer(), nullable=False),
        sa.Column("receiver_id", sa.Integer(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column(
            "sent_date", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_messages_id"), "messages", ["id"])


def downgrade() -> None:
    op.drop_table("messages")
    op.drop_table("applications")
    op.drop_table("offers")
    op.drop_table("experiences")
    op.drop_table("diplomas")
    op.drop_table("sports_organizations")
    op.drop_table("athlete_profiles")

    op.execute("DROP TYPE IF EXISTS offerstatus")
    op.execute("DROP TYPE IF EXISTS applicationstatus")
