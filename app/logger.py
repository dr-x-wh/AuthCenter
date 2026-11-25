import logging

from app.core import config

logger = logging.getLogger("app")


def init() -> None:
    settings = config.get_settings()
    logging.basicConfig(level=settings.log_level, format="%(asctime)s | %(levelname)s | %(module)s:%(lineno)d | %(message)s", )
