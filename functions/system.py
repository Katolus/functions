import json
import os
from pathlib import Path

from functions import defaults
from functions import logs
from functions.config.models import FunctionConfig
from functions.constants import ConfigName
from functions.constants import PACKAGE_CONFIG_DIR_PATH
from functions.constants import SignatureType
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


def add_required_files(
    function_name: str,
    function_dir: str,
    *,
    main_content: str,
    signature_type: SignatureType,
) -> FunctionConfig:
    """Add required files into the function directory"""
    # Get file contents before creating any system objects
    function_config = defaults.default_config(
        function_name, function_dir, signature_type
    )
    config_content = json.dumps(function_config.dict())

    # Make a new directory
    make_dir(function_dir)
    # Create a confing setup
    add_file(
        function_dir,
        filename="config.json",
        content=config_content,
    )

    # Create a Docker file
    add_file(function_dir, filename="Dockerfile", content=defaults.default_docker_file)

    # Create a docker ignore file
    add_file(
        function_dir,
        filename=".dockerignore",
        content=defaults.default_docker_ignore_file,
    )

    # Create a docker ignore file
    add_file(
        function_dir,
        filename="requirements.txt",
        content=defaults.default_requirements_file,
    )

    # Create a default entry point
    add_file(function_dir, filename="main.py", content=main_content)

    return function_config


def write_to_file(filepath: PathStr, content: str) -> None:
    """Writes content to a file."""
    with open(filepath, "w") as file:
        file.write(content)


def check_if_file_exists(filepath: PathStr) -> bool:
    """Checks if a file exists."""
    return Path(filepath).exists()


def construct_filepath_in_config_dir(filename: str) -> str:
    """Construct a config filepath based on the system's default config path."""
    return os.path.join(PACKAGE_CONFIG_DIR_PATH, filename)
