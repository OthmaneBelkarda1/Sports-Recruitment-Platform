"""Run-time schema migration for the inheritance refactoring.

Transforms the old schema (separate `users` + `athlete_profiles` + `sports_organizations`)
into the new schema where profile tables inherit user columns directly.
"""
from sqlalchemy import text


async def _table_exists(conn, name: str) -> bool:
    result = await conn.execute(
        text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = :name)"),
        {"name": name},
    )
    return result.scalar()


async def _column_exists(conn, table: str, column: str) -> bool:
    result = await conn.execute(
        text(
            "SELECT EXISTS (SELECT FROM information_schema.columns "
            "WHERE table_name = :table AND column_name = :column)"
        ),
        {"table": table, "column": column},
    )
    return result.scalar()


async def _index_exists(conn, index_name: str) -> bool:
    result = await conn.execute(
        text("SELECT EXISTS (SELECT FROM pg_indexes WHERE indexname = :name)"),
        {"name": index_name},
    )
    return result.scalar()


async def _constraint_exists(conn, constraint: str) -> bool:
    result = await conn.execute(
        text(
            "SELECT EXISTS (SELECT FROM information_schema.table_constraints "
            "WHERE constraint_name = :name)"
        ),
        {"name": constraint},
    )
    return result.scalar()


async def _fk_to_users_exists(conn, table: str, column: str) -> bool:
    result = await conn.execute(
        text(
            "SELECT EXISTS (SELECT 1 FROM information_schema.table_constraints tc "
            "JOIN information_schema.key_column_usage kcu USING (constraint_name, table_schema, table_name) "
            "JOIN information_schema.constraint_column_usage ccu "
            "  USING (constraint_name, table_schema, table_name) "
            "WHERE tc.constraint_type = 'FOREIGN KEY' "
            "AND tc.table_name = :table AND kcu.column_name = :column "
            "AND ccu.table_name = 'users')"
        ),
        {"table": table, "column": column},
    )
    return result.scalar()


async def _ensure_messages_types(conn) -> None:
    if not await _column_exists(conn, "messages", "sender_type"):
        await conn.execute(
            text("ALTER TABLE messages ADD COLUMN sender_type VARCHAR(20) NOT NULL DEFAULT 'athlete'")
        )
        await conn.execute(
            text("ALTER TABLE messages ADD COLUMN receiver_type VARCHAR(20) NOT NULL DEFAULT 'athlete'")
        )


async def migrate_schema(conn):
    """Upgrade old schema to new inheritance-based schema."""
    users_exists = await _table_exists(conn, "users")
    if not users_exists:
        await _ensure_messages_types(conn)
        return

    profiles_have_email = await _column_exists(conn, "athlete_profiles", "email")
    if profiles_have_email:
        await _ensure_messages_types(conn)
        return

    user_columns = [
        ("email", "VARCHAR(255)"),
        ("password_hash", "VARCHAR(255)"),
        ("auth_token", "VARCHAR(255)"),
        ("created_at", "TIMESTAMPTZ"),
        ("is_active", "BOOLEAN"),
    ]

    for col, dtype in user_columns:
        await conn.execute(text(f"ALTER TABLE athlete_profiles ADD COLUMN IF NOT EXISTS {col} {dtype}"))
        await conn.execute(text(f"ALTER TABLE sports_organizations ADD COLUMN IF NOT EXISTS {col} {dtype}"))

    await conn.execute(
        text(
            "UPDATE athlete_profiles SET "
            "email = u.email, password_hash = u.password_hash, "
            "auth_token = u.auth_token, created_at = u.created_at, "
            "is_active = u.is_active "
            "FROM users u WHERE athlete_profiles.user_id = u.id"
        )
    )
    await conn.execute(
        text(
            "UPDATE sports_organizations SET "
            "email = u.email, password_hash = u.password_hash, "
            "auth_token = u.auth_token, created_at = u.created_at, "
            "is_active = u.is_active "
            "FROM users u WHERE sports_organizations.user_id = u.id"
        )
    )

    await conn.execute(text("ALTER TABLE athlete_profiles ALTER COLUMN email SET NOT NULL"))
    await conn.execute(text("ALTER TABLE athlete_profiles ALTER COLUMN password_hash SET NOT NULL"))
    await conn.execute(text("ALTER TABLE athlete_profiles ALTER COLUMN created_at SET DEFAULT NOW()"))
    await conn.execute(text("ALTER TABLE athlete_profiles ALTER COLUMN is_active SET DEFAULT TRUE"))
    await conn.execute(text("ALTER TABLE sports_organizations ALTER COLUMN email SET NOT NULL"))
    await conn.execute(text("ALTER TABLE sports_organizations ALTER COLUMN password_hash SET NOT NULL"))
    await conn.execute(text("ALTER TABLE sports_organizations ALTER COLUMN created_at SET DEFAULT NOW()"))
    await conn.execute(text("ALTER TABLE sports_organizations ALTER COLUMN is_active SET DEFAULT TRUE"))

    fk_sender = await _fk_to_users_exists(conn, "messages", "sender_id")
    if fk_sender:
        await conn.execute(text("ALTER TABLE messages DROP CONSTRAINT IF EXISTS messages_sender_id_fkey"))
        await conn.execute(text("ALTER TABLE messages DROP CONSTRAINT IF EXISTS messages_receiver_id_fkey"))

    for tbl in ("athlete_profiles", "sports_organizations"):
        await conn.execute(text(f"ALTER TABLE {tbl} DROP CONSTRAINT IF EXISTS {tbl}_user_id_key"))
        await conn.execute(text(f"ALTER TABLE {tbl} DROP CONSTRAINT IF EXISTS {tbl}_user_id_fkey"))

    await conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
    await conn.execute(text("DROP TYPE IF EXISTS userrole"))

    await conn.execute(text("ALTER TABLE athlete_profiles DROP COLUMN IF EXISTS user_id"))
    await conn.execute(text("ALTER TABLE sports_organizations DROP COLUMN IF EXISTS user_id"))

    for idx in ("ix_athlete_profiles_id", "ix_sports_organizations_id",
                "ix_diplomas_id", "ix_experiences_id", "ix_offers_id",
                "ix_applications_id", "ix_messages_id"):
        if await _index_exists(conn, idx):
            await conn.execute(text(f"DROP INDEX IF EXISTS {idx}"))

    await conn.execute(
        text("CREATE UNIQUE INDEX IF NOT EXISTS ix_athlete_profiles_email ON athlete_profiles (email)")
    )
    await conn.execute(
        text("CREATE UNIQUE INDEX IF NOT EXISTS ix_sports_organizations_email ON sports_organizations (email)")
    )

    await _ensure_messages_types(conn)
