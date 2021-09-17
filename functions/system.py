import json
import os
from pathlib import Path
from typing import Optional
from typing import Union

from pydantic import DirectoryPath
from pydantic import validate_arguments

from functions import defaults
from functions.constants import ConfigName
from functions.types import FunctionConfig, LocalFunctionPath


@validate_arguments
def load_config(config_dir: LocalFunctionPath) -> FunctionConfig:
    """Load a configuration file into a Python object."""
    config = None
    with open(construct_config_path(config_dir, ConfigName.BASE), "r") as file:
        config = json.load(file)

    return FunctionConfig(path=str(config_dir), **config)


def get_full_path(function_path: Union[Path, str]) -> LocalFunctionPath:
    """Returns a full path of a function"""
    return LocalFunctionPath(os.path.abspath(os.path.join(os.getcwd(), function_path)))


def construct_config_path(
    full_path: Path, config_name: str = ConfigName.BASE
) -> LocalFunctionPath:
    """Returns a configuration file path"""
    return LocalFunctionPath(os.path.join(full_path, config_name))


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


def add_required_files(
    function_name: str, function_dir: str, *, main_content: str, signature_type: str
):
    """Add required files into the function directory"""
    # Make a new directory
    make_dir(function_dir)
    # Create a confing setup
    add_file(
        function_dir,
        filename="config.json",
        content=json.dumps(defaults.default_config(function_name, signature_type)),
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
