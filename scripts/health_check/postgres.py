import sys

from sqlalchemy import (
    create_engine,
    text,
)

from app.core.config import (
    settings,
)


def check_connection() -> tuple[bool, str]:
    """Check the PostgreSQL connection.

    Returns
    -------
    tuple[bool, str]
        status, message
    """
    engine = create_engine(
        f"postgresql://{settings.db.username}:{settings.db.password}@"
        f"{settings.db.host}:{settings.db.port}/{settings.db.tablename}"
    )

    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        version: str = result.scalar().split(",", maxsplit=1)[0]  # type: ignore[reportOptionalMemberAccess]

    return True, f"✅ PostgreSQL is available (version: {version})"


if __name__ == "__main__":
    print("🐘 PostgreSQL check...")

    try:
        ok, msg = check_connection()
    except Exception as e:
        ok, msg = False, f"❌ PostgreSQL check failed:\n{e!s}"

    print(msg)
    sys.exit(not ok)
