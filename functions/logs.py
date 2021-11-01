"""
Holds functions and information in regards to the loggining features.

https://docs.python.org/3/howto/logging.html#when-to-use-logging
https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook

"""
import logging
import os
from logging.handlers import RotatingFileHandler

from functions.constants import DEFAULT_LOG_FILE
from functions.constants import LoggingLevel
from functions.constants import PACKAGE_CONFIG_DIR_PATH

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

LOGGING_LEVELS = {
    LoggingLevel.INFO: logging.INFO,
    LoggingLevel.DEBUG: logging.DEBUG,
    LoggingLevel.WARNING: logging.WARNING,
    LoggingLevel.ERROR: logging.ERROR,
}


# Set up the console handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_handler.setFormatter(logging.Formatter("%(message)s"))
logger.addHandler(c_handler)

# Set up the file handler
f_handler = RotatingFileHandler(
    filename=os.path.join(PACKAGE_CONFIG_DIR_PATH, DEFAULT_LOG_FILE),
    backupCount=3,
    maxBytes=1000000,
    mode="a",
    delay=True,
)
f_handler.setLevel(logging.DEBUG)
f_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
)
logger.addHandler(f_handler)


def set_console_handler_level(level: LoggingLevel = LoggingLevel.INFO) -> None:
    """Set console logging level for the application."""
    log_level = LOGGING_LEVELS[level]
    c_handler.setLevel(log_level)


def debug(msg: str) -> None:
    """Use this level for anything that happens in the program."""
    logger.debug(msg)


def info(msg: str) -> None:
    """Use this level to record all actions that are user driven or system specific."""
    logger.info(msg)


def warning(msg: str) -> None:
    """Use this level to record all irregular or undesired actions."""
    logger.warning(msg)


def error(msg: str) -> None:
    """Use this level to record any error that occurs."""
    logger.error(msg)


def exception(msg: str) -> None:
    """Use this when you want to report an error with a stacktrace."""
    logger.exception(msg)


def remove_empty_lines_from_string(string: str) -> str:
    """Remove empty lines from a string."""
    return "".join(string.splitlines()).strip()
