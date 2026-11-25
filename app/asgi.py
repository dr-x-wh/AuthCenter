from app.core import Settings
from app.factory import create_app

settings = Settings(
    _env_file=".env" if __name__ == "__main__" else None,
    _env_file_encoding="utf-8",
)
app = create_app(settings)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host=str(settings.host),
        port=settings.port,
        log_level=settings.log_level,
    )
