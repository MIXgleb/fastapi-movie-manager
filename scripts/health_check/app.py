import sys
from time import sleep

import httpx

from app.core.config import settings

TIMEOUT = 2  # seconds
SUCCESS_CODES = {200}


def check_connection() -> tuple[bool, str]:
    """Check the FastAPI application connection.

    Returns
    -------
    tuple[bool, str]
        status, message
    """
    health_check_url = f"http://{settings.app.host}:{settings.app.port}/health/check"

    with httpx.Client() as client:
        for _ in range(3):
            response = client.get(health_check_url, timeout=TIMEOUT)

            if response.status_code in SUCCESS_CODES:
                break

            sleep(1)
        else:
            return False, f"❌ FastAPI returned HTTP {response.status_code}"  # type: ignore[reportPossiblyUnboundVariable]

    return True, f"✅ FastAPI is available (HTTP {response.status_code})"


if __name__ == "__main__":
    print("🚀 FastAPI application check...")

    try:
        ok, msg = check_connection()
    except Exception as e:
        ok, msg = False, f"❌ FastAPI check failed:\n{e!s}"

    print(msg)
    sys.exit(not ok)
