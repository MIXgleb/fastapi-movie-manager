import sys

import redis

from app.core.config import settings


def check_connection() -> tuple[bool, str]:
    """Check the redis connection.

    Returns
    -------
    tuple[bool, str]
        status, message
    """
    redis_conn = redis.Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        socket_timeout=2,
        decode_responses=True,
        encoding=settings.redis.encoding,
    )

    if not redis_conn.ping():
        return False, "❌ Redis is not responding"

    info: dict[str, str] = redis_conn.info()  # type: ignore[reportAssignmentType]
    version = info.get("redis_version", "unknown")
    used_memory = info.get("used_memory_human", "unknown")

    return (
        True,
        f"✅ Redis is available (version: {version}, used memory: {used_memory})",
    )


if __name__ == "__main__":
    print("🧠 Redis check...")

    try:
        ok, msg = check_connection()
    except Exception as e:
        ok, msg = False, f"❌ Redis check failed:\n{e!s}"

    print(msg)
    sys.exit(not ok)
