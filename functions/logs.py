"""
Holds functions and information in regards to the loggining features.

https://docs.python.org/3/howto/logging.html#when-to-use-logging
https://docs.python.org/3/howto/logging-cookbook.html#logging-cookbook

"""
import logging
from logging.handlers import RotatingFileHandler

from functions.constants import DEFAULT_LOG_FILEPATH
from functions.constants import LoggingLevel

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

LOGGING_LEVELS = {
    LoggingLevel.INFO: logging.INFO,
    LoggingLevel.DEBUG: logging.DEBUG,
    LoggingLevel.WARNING: logging.WARNING,
    LoggingLevel.ERROR: logging.ERROR,
}


class ConsoleFilter(logging.Filter):
    """Filter that only allows messages with a specific level to be printed to the console."""

    def __init__(self, level: LoggingLevel):
        super().__init__()
        self.level = LOGGING_LEVELS[level]

    def filter(self, record: logging.LogRecord) -> bool:
        """Return True if the record is at the level of the filter."""
        return record.levelno == self.level


# Set up the console handler
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.INFO)
c_handler.setFormatter(logging.Formatter("%(message)s"))

c_filter = ConsoleFilter(LoggingLevel.INFO)
c_handler.addFilter(c_filter)
logger.addHandler(c_handler)

# Set up the file handler
f_handler = RotatingFileHandler(
    filename=DEFAULT_LOG_FILEPATH,
    backupCount=3,
    maxBytes=1000000,
    mode="a",
    delay=True,
)
f_handler.setLevel(logging.DEBUG)
f_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
logger.addHandler(f_handler)


def set_console_debug_level() -> None:
    """Set console logging level for the application."""
    c_handler.removeFilter(c_filter)
    c_handler.setLevel(logging.DEBUG)


def debug(msg: str) -> None:
    """Use this level for anything that happens in the program."""
    logger.debug(msg)


def info(msg: str) -> None:
    """Use this level to record all actions that are user driven or system specific."""
    logger.info(msg)


def warning(msg: str) -> None:
    """Use this level to record all irregular or undesired actions."""
    logger.warning(msg)


def error(error: object) -> None:
    """Use this level to record any error that occurs."""
    logger.error(error)


def exception(error: object) -> None:
    """Use this when you want to report an error with a stacktrace."""
    logger.exception(error)


def remove_empty_lines_from_string(string: str) -> str:
    """Remove empty lines from a string."""
    return "".join(string.splitlines()).strip()
