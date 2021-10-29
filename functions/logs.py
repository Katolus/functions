"""
Holds functions and information in regards to the loggining features.

https://docs.python.org/3/howto/logging.html#when-to-use-logging
https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook

"""

import logging
from logging.handlers import RotatingFileHandler
import os
from typing import List
import warnings

from functions.constants import APP_CONFIG_PATH
from functions.constants import LoggingLevel

logger = logging.getLogger(__name__)


# File logger
log_name = "functions.log"
log_path = os.path.join(APP_CONFIG_PATH, log_name)

f_handler = RotatingFileHandler(
    log_path,
    backupCount=3,
    maxBytes=1000000,
    mode="a",
)
f_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
f_handler.setLevel(logging.INFO)
f_handler.setFormatter(f_formatter)

# Console logger
c_handler = logging.StreamHandler()
c_formatter = logging.Formatter("%(message)s")
c_handler.setLevel(logging.INFO)
c_handler.setFormatter(c_formatter)


handlers: List[logging.Handler] = [f_handler, c_handler]


# Add handlers to the logger
for handler in handlers:
    logger.addHandler(handler)


LOGGING_LEVELS = {
    LoggingLevel.INFO: logging.INFO,
    LoggingLevel.DEBUG: logging.DEBUG,
    LoggingLevel.WARNING: logging.WARNING,
    LoggingLevel.ERROR: logging.ERROR,
}


def set_logger_level(level: LoggingLevel = LoggingLevel.INFO) -> None:
    """Set logging level for the application."""
    log_level = LOGGING_LEVELS[level]

    logger.setLevel(log_level)
    for handler in handlers:
        handler.setLevel(log_level)


def debug(msg: str) -> None:
    """Use this level for anything that happens in the program."""
    logger.debug(msg)


def info(msg: str) -> None:
    """Use this level to record all actions that are user driven or system specific."""
    logger.info(msg)


def warning(msg: str) -> None:
    """Use this level to record all irregular or undesired actions."""
    logger.warning(msg)


def warn(msg: str, **kwargs) -> None:
    """Warn a user instead of"""
    warnings.warn(msg, **kwargs)


def error(msg: str) -> None:
    """Use this level to record any error that occurs."""
    logger.error(msg)


def exception(msg: str) -> None:
    """Use this when you want to report an error with a stacktrace."""
    logger.exception(msg)
