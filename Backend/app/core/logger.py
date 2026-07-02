import logging
import sys

from app.core.config import settings


def setup_logger() -> logging.Logger:
    """
    Configure and return the application's root logger.
    """

    logger = logging.getLogger("app")

    if logger.hasHandlers():
        return logger

    log_level = logging.DEBUG if settings.debug else logging.INFO

    logger.setLevel(log_level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


logger = setup_logger()