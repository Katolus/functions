import os
from typing import Dict

from pydantic import DirectoryPath
from pydantic import validate_arguments

from functions.system import get_config_path
from functions.docker import DockerImage


@validate_arguments
def validate_dir(function_dir: DirectoryPath):
    # Check if config exists
    config_path = get_config_path(function_dir)

    if not config_path:
        raise ValueError(f"No config file found at {function_dir}")


def validate_image(image: DockerImage):
    # TODO: Validate an image being suitable for use, consider pydantic for the job
    ...

def valid_function_dirs() -> Dict[str, str]:
    """Returns a List of valid function directories."""
    list_of_function_dirs = {}
    for dir_entry in os.scandir("."):
        if dir_entry.is_dir():
            config_path = get_config_path(dir_entry)
            if config_path:
                list_of_function_dirs[dir_entry.name] = config_path
    return list_of_function_dirs
