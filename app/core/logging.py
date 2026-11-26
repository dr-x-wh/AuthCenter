import logging

from uvicorn.logging import DefaultFormatter

logger = logging.getLogger("app")


def configure_logging(level: str) -> None:
    handler = logging.StreamHandler()

    handler.setFormatter(
        DefaultFormatter(
            fmt="%(levelprefix)s %(asctime)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            use_colors=True,
        )
    )

    logging.basicConfig(
        level=level,
        handlers=[handler],
        force=True,
    )

    logger.setLevel(level)
