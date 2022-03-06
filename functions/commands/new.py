import os
from pathlib import Path

import typer

from functions import user
from functions.callbacks import check_if_name_is_a_valid_string
from functions.callbacks import confirm_current_directory_as_target
from functions.config.models import FunctionRecord
from functions.constants import LocalStatus
from functions.core import FTyper
from functions.defaults import Defaults

app = FTyper(help="Create new templated functions.")


@app.command()
def pubsub(
    function_name: str = typer.Argument(
        ...,
        help="The name of the function to create",
        callback=check_if_name_is_a_valid_string,
    ),
    function_dir: Path = typer.Option(
        None,
        "--dir",
        exists=True,
        file_okay=False,
        resolve_path=True,
        callback=confirm_current_directory_as_target,
        help="Path that will be used as a root path for the new function's files",
    ),
) -> None:
    """
    Create a new function that uses Google Cloud Pub/Sub as a trigger.
    """
    full_function_path = os.path.join(function_dir, function_name)

    # Get the default class for this type of function
    pubsub = Defaults.GCP.CloudFunction.PubSub

    # Generate the config instance
    pubsub_config = pubsub.config(function_name, full_function_path)

    # Create a function record
    f_record = FunctionRecord(name=function_name, config=pubsub_config)

    # Generate required files
    pubsub.generate_required_files(f_record)

    # Prompt about saving the config file inside the function's directory
    user.prompt_to_save_config(pubsub_config)

    # Add function to the function registry
    f_record.set_local_status(LocalStatus.NEW)
    f_record.update_registry()

    user.inform(f"Added a new pubsub function -> {full_function_path}")


@app.command()
def http(
    function_name: str = typer.Argument(
        ...,
        help="The name of the function to create",
        callback=check_if_name_is_a_valid_string,
    ),
    function_dir: Path = typer.Option(
        None,
        "--dir",
        exists=True,
        file_okay=False,
        resolve_path=True,
        callback=confirm_current_directory_as_target,
        help="Path that will be used as a root path for the new function's files",
    ),
) -> None:
    """
    Create a new function that uses HTTP as a trigger.
    """
    full_function_path = os.path.join(function_dir, function_name)

    # Get the default class for this type of function
    http = Defaults.GCP.CloudFunction.HTTP

    # Generate the config instance
    http_config = http.config(function_name, full_function_path)

    # Create a function record
    f_record = FunctionRecord(name=function_name, config=http_config)

    # Generate required files
    http.generate_required_files(f_record)

    # Prompt about saving the config file inside the function's directory
    user.prompt_to_save_config(http_config)

    # Add function to the function registry
    f_record.set_local_status(LocalStatus.NEW)
    f_record.update_registry()

    user.inform(f"Added a new http function to -> {full_function_path}")
