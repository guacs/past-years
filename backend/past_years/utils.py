"""Utilities common to the entire application."""
import sys
from loguru import logger

from . import config


def configure_logger():
    """Configures the Loguru logger."""

    log_config = config.get_logs_config()

    loguru_config: dict[str, list | dict] = {
        "handlers": [
            {
                "sink": sys.stdout,
                "format": log_config.format,
                "colorize": True,
                "level": log_config.log_level.upper(),
                "serialize": log_config.serialize,
            },
            {
                "sink": f"{log_config.sink}",
                "format": log_config.format,
                "colorize": False,
                "enqueue": True,
                "level": log_config.log_level.upper(),
            },
        ],
        "extra": {"request_id": "0000-0000-0000-0000"},
    }

    logger.configure(**loguru_config)


"""
config: dict[str, list | dict] = {
        "handlers": [
            {
                "sink": sys.stdout,
                "format": logger_config.format,
                "colorize": True,
                "level": logger_config.log_level.upper(),
            },
            {
                "sink": f"{logger_config.sink}",
                "format": logger_config.format,
                "colorize": False,
                "enqueue": True,
                "level": logger_config.log_level.upper(),
            },
        ],
        "extra": {"request_id": "0000-0000-0000-0000"},
    }
"""
