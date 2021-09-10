import json
import fnmatch
import os
from pathlib import Path
from typing import Optional
from typing import Union

from pydantic import DirectoryPath
from pydantic import FilePath
from pydantic import validate_arguments

from functions.hints import Config


@validate_arguments
def load_config(config_path: FilePath) -> Config:
    """Load a configuration file into a Python object."""
    config = None
    with open(config_path, "r") as file:
        config = json.load(file)

    return Config(**config)


def get_config_path(dir_path: Union[os.DirEntry, DirectoryPath]) -> Optional[str]:
    """Returns a config path if present."""
    for filename in os.listdir(dir_path):
        if fnmatch.fnmatch(filename, "config.json"):
            return os.path.join(dir_path, filename)
    return None


def get_full_path(function_path: str) -> Path:
    """Returns a full path of a function"""
    return Path(os.path.abspath(os.path.join(os.getcwd(), function_path)))


def construct_config_path(full_path: Path, config_name: str) -> Path:
    """Returns a configuration file path"""
    return Path(os.path.join(full_path, config_name))


def make_dir(function_dir: str):
    """Creates a directory will throw an error if a directory exists already."""
    os.makedirs(function_dir, exist_ok=False)


def add_file(function_dir: str, *, filename: str, content: str):
    """Adds a file into a directory with given content"""
    with open(os.path.join(function_dir, filename), "w") as file:
        file.write(content)


def link_common(function_dir: str):
    """Links common folder to the new function directory."""
    common_folder_name = "common"
    src_path = os.path.abspath(common_folder_name)
    dst_path = os.path.abspath(os.path.join(function_dir, common_folder_name))
    os.symlink(src_path, dst_path, target_is_directory=False)
