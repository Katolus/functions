import os
import json
from typing import Optional
import functions

import typer

from functions import defaults

app = typer.Typer(help="Factory method for creating new functions")


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


@app.command()
def pubsub(
    # TODO Add validatation to make sure this is not a path
    function_name: str,
    dir: str = typer.Option(
        ".", help="Directory that will be used as a root of the new function"
    ),
):
    """Creates a new pubsub directory"""
    # Make a new directory
    function_dir = os.path.join(dir, function_name)
    make_dir(function_dir)
    # Create a confing setup
    add_file(
        function_dir,
        filename="config.json",
        content=json.dumps(defaults.default_config(function_name)),
    )

    # Create a default entry point
    add_file(function_dir, filename="main.py", content=defaults.default_pubsub_entry)

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

    # Links common folder
    # link_common(function_dir)
    # TODO: Print path


if __name__ == "__main__":
    app()
