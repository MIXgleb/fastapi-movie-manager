import uvicorn

from app.core import (
    settings,
)


def main() -> None:
    """Launch the ASGI web server."""
    uvicorn.run(
        app="app:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=True,
    )


if __name__ == "__main__":
    main()
