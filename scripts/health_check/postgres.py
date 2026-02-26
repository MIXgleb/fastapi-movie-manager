import sys

from sqlalchemy.engine import (
    URL,
    create_engine,
)
from sqlalchemy.sql.expression import (
    text,
)

from app.core import (
    settings,
)


def check_connection() -> tuple[bool, str]:
    """
    Check the PostgreSQL connection.

    Returns
    -------
    tuple[bool, str]
        status, message
    """
    engine = create_engine(
        url=URL.create(
            drivername="postgresql",
            username=settings.db.username,
            password=settings.db.password.get_secret_value(),
            host=settings.db.host,
            port=settings.db.port,
            database=settings.db.database,
        ),
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
