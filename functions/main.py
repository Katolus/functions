import os
from pathlib import Path
from typing import Optional

import typer

from functions import logs
from functions import styles
from functions import user
from functions.autocomplete import autocomplete_function_names
from functions.autocomplete import autocomplete_running_function_names
from functions.callbacks import add_callback
from functions.callbacks import build_function_callack
from functions.callbacks import function_name_autocomplete_callback
from functions.callbacks import remove_function_name_callback
from functions.callbacks import running_functions_autocomplete_callback
from functions.callbacks import version_callback
from functions.commands import gcp
from functions.commands import new
from functions.config import remove_function_from_registry
from functions.config import store_function_info_to_registry
from functions.config.files import FunctionRegistry
from functions.config.models import FunctionConfig
from functions.constants import FunctionStatus
from functions.constants import FunctionType
from functions.constants import LoggingLevel
from functions.core import Functions
from functions.docker.helpers import all_functions
from functions.docker.helpers import get_config_from_image
from functions.docker.tools import build_image
from functions.docker.tools import get_image
from functions.docker.tools import remove_image
from functions.docker.tools import run_container
from functions.docker.tools import stop_container
from functions.gcp.cloud_function.errors import GCPCommandError
from functions.gcp.helpers import check_if_gcloud_cmd_installed
from functions.logs import set_console_debug_level
from functions.styles import green
from functions.system import construct_abs_path

subcommands = [(new.app, "new")]

# Only add gcp commands if gcloud is installed
if check_if_gcloud_cmd_installed():
    subcommands.append((gcp.app, "gcp"))

app = Functions(subcommands=subcommands)


@app.callback()
def main(
    verbose: bool = typer.Option(
        False,
        "--verbose",
        help="Sets the conext of the command to be verbose",
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        help="Prints out the version of the package",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """
    Manage users in the awesome CLI app.
    """
    log_level = LoggingLevel.INFO
    if verbose:
        app.state.verbose = True
        log_level = LoggingLevel.DEBUG
        set_console_debug_level()

    logs.debug(f"Running application in {log_level} logging level.")


@app.command()
def error() -> None:
    """A command for testing error messages"""
    user.inform("Message before the error")
    raise GCPCommandError(error_msg="Throwing an error in a test command")


@app.command()
def build(
    function_dir: Path = typer.Argument(
        ...,
        help="Path to  a function's directory you want to build",
        exists=True,
        file_okay=False,
        resolve_path=True,
        callback=build_function_callack,
    ),
    show_logs: bool = typer.Option(False, "--show-logs", help="Show build logs"),
) -> None:
    """Builds an image of a given function"""
    # Get the absolute path
    full_path = construct_abs_path(function_dir)

    # Load configuration
    config = FunctionConfig.load(full_path)

    _ = build_image(config, show_logs)

    function_name = config.run_variables.name
    # store the function details in the config
    store_function_info_to_registry(function_name, config, FunctionStatus.BUILT)

    user.inform(
        f"{styles.green('Successfully')} build a function's image."
        f" The name of the functions is -> {function_name}"
    )


@app.command()
def run(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to run",
        autocompletion=autocomplete_function_names,
        callback=function_name_autocomplete_callback,
    ),
) -> None:
    """Start a container for a given function"""

    function_image = get_image(function_name)
    config = get_config_from_image(function_image)
    container = run_container(function_image, config)

    user.inform(
        f"Function ({container.name}) has {green('started')}."
        f" Visit -> http://localhost:{config.run_variables.port}"
    )


@app.command()
def stop(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to stop",
        autocompletion=autocomplete_running_function_names,
        callback=running_functions_autocomplete_callback,
    ),
) -> None:
    """Stops a running function"""
    stop_container(function_name)
    user.inform(f"Function ({function_name}) has been stopped.")


@app.command("list")
def list_functions() -> None:
    """List existing functions"""
    # TODO: Merge docker images and registry functions together
    # functions = all_functions()
    functions = FunctionRegistry.fetch_all_functions()

    # Check if a function is running at the moment
    if functions:
        # Pluralize the word functions based on the number of functions
        plural_function = "functions" if len(functions) > 1 else "function"

        user.inform(f"We found {len(functions)} {plural_function}\n")
        for function in functions:
            user.inform(str(function))
    else:
        user.inform("No functions found")


@app.command()
def remove(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to remove",
        autocompletion=autocomplete_function_names,
        callback=remove_function_name_callback,
    )
) -> None:
    """Removes an image of a functions from the local registry"""
    remove_image(function_name)
    remove_function_from_registry(function_name)
    user.inform(f"Function ({function_name}) has been removed")


@app.command()
def config() -> None:
    """Renders function's configuration file into the command line"""
    raise NotImplementedError()


@app.command()
def rebuild(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to rebuild",
        autocompletion=autocomplete_function_names,
    ),
    show_logs: bool = typer.Option(False, "--show-logs", help="Show build logs"),
) -> None:
    """Rebuild a function if it is possible"""
    functions = all_functions()

    for function in functions:
        if function.name == function_name:
            build_image(function.config, show_logs)
            raise typer.Exit()

    user.inform("No functions found")


@app.command()
def add(
    function_dir: Path = typer.Argument(
        ...,
        help="Path to a function's directory you want to add",
        exists=True,
        file_okay=False,
        resolve_path=True,
        callback=add_callback,
    ),
) -> None:
    """Adds a function to the registry"""
    # Get the absolute path
    abs_path = construct_abs_path(function_dir)
    dir_name = os.path.basename(abs_path)

    # Ask the user for a function name if not provided and present a default
    function_name = user.ask(
        "What should be the name of the function?",
        default=dir_name,
    )

    # Check if the config file exists
    if FunctionConfig.check_config_file_exists(abs_path):
        # Load the config file
        config = FunctionConfig.load(abs_path)
    else:
        # Ask what type of function it is
        function_type = user.ask(
            "What type of function is this?",
            default=FunctionType.HTTP,
            options=FunctionType.options(),
        )
        # Generate a config instance
        config = FunctionConfig.generate(function_type, abs_path)

    # Load the config file if exists otherwise generate a new one

    # Check if the function is already in the registry based on the name

    # Check if the function is already in the registry based on the path

    # If it does not exist, add it to the registry

    # If it does exist, ask the user if he wants to overwrite it

    # Load configuration
    config = FunctionConfig.load(abs_path)

    # store the function details in the config
    store_function_info_to_registry(function_name, config, FunctionStatus.ADDED)

    user.inform(
        f"{styles.green('Successfully')} added a function to the registry."
        f" The name of the functions is -> {function_name}"
    )
