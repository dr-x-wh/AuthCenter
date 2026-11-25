import logging

logger = logging.getLogger("app")


def configure_logging(level: str) -> None:
    logging.basicConfig(level=level, format="%(name)s %(asctime)s %(levelname)s: %(message)s")
    logger.setLevel(level)
