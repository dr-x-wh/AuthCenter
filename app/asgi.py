import uvicorn
from pydantic import ValidationError

from app.core import Settings
from app.factory import create_app


def main() -> None:
    try:
        settings = Settings()
    except ValidationError as exc:
        errors = "\n".join(
            f"{error['loc'][0]}: {error['msg']}"
            for error in exc.errors(include_input=False, include_context=False)
        )
        raise SystemExit(f"Invalid backend configuration\n{errors}") from None

    uvicorn.run(
        create_app(settings),
        host=str(settings.host),
        port=settings.port,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
