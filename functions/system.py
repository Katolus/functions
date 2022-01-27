import os
import time
from pathlib import Path
from typing import Iterable, TextIO

from functions import logs
from functions.constants import ConfigName
from functions.constants import PACKAGE_CONFIG_DIR_PATH
from functions.types import PathStr


def construct_abs_path(path: PathStr) -> Path:
    """Returns an absolute path of a path"""
    return Path(os.path.abspath(os.path.join(os.getcwd(), path)))


# Deprecated
def construct_config_path(
    full_path: PathStr, config_name: str = ConfigName.BASE
) -> Path:
    """Returns a configuration file path"""
    return Path(os.path.join(full_path, config_name))


def make_dir(function_dir: str) -> None:
    """Makes a directory or skips if already exists"""
    if not os.path.exists(function_dir):
        os.makedirs(function_dir)
        logs.debug(f"Created directory {function_dir}")


# Consider using the write to file method instead of this
def add_file(function_dir: str, filename: str, content: str):
    """Adds a file into a directory with given content"""
    logs.debug(f"Adding file {filename} to {function_dir}")
    with open(os.path.join(function_dir, filename), "w") as file:
        file.write(content)


def write_to_file(filepath: PathStr, content: str) -> None:
    """Writes content to a file."""
    logs.debug(f"Writing to file {filepath}")
    with open(filepath, "w") as file:
        file.write(content)


def check_if_file_exists(filepath: PathStr) -> bool:
    """Checks if a file exists."""
    return Path(filepath).exists()


def construct_filepath_in_config_dir(filename: str) -> str:
    """Construct a config filepath based on the system's default config path."""
    return os.path.join(PACKAGE_CONFIG_DIR_PATH, filename)


def follow_file(file: TextIO, sleep_sec: float = 0.1) -> Iterable[str]:
    """Follows a file and returns content line by line."""

    line: str = ""
    while True:
        tmp = file.readline()

        if tmp is not None:
            line += tmp
            if line.endswith("\n"):
                yield line
                line = ""
            else:
                time.sleep(sleep_sec)
