from pathlib import Path
from typing import Optional

import typer

from functions import user
from functions.autocomplete import autocomplete_deploy_functions
from functions.constants import CloudServiceType
from functions.gcp.other import delete_function
from functions.gcp.other import deploy_function
from functions.gcp.other import read_logs
from functions.services import describe_function
from functions.system import load_config

app = typer.Typer(help="Deploy functions in GCP")


@app.command()
def install() -> None:
    """Install required libraries"""
    raise NotImplementedError()


@app.command()
def update() -> None:
    """Update required libraries"""
    raise NotImplementedError()


@app.command()
def deploy(
    function_dir: Path = typer.Argument(
        ...,
        # It would be great if it supported both image name and path
        autocompletion=autocomplete_deploy_functions,
        exists=True,
        file_okay=False,
        help="Path to the functions you want to deploy",
        resolve_path=True,
    ),
    service: Optional[CloudServiceType] = typer.Option(
        None,
        help="Type of service you want this resource to be deploy to",
        autocompletion=CloudServiceType.all,
    ),
) -> None:
    """Deploy a functions to GCP"""
    config = load_config(function_dir)
    service_type = service or config.deploy_variables.service

    deploy_function(config, CloudServiceType(service_type))

    user.inform(f"{config.run_variables.name} functions has been deployed to GCP!")


@app.command()
def delete(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to remove",
    ),
) -> None:
    """Deletes a functions deployed to GCP"""
    user.confirm_abort(f"Are you sure you want to remove '{function_name}'?")
    delete_function(function_name)


@app.command()
def describe(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to describe",
    ),
) -> None:
    """Returns information about a deployed function"""
    describe_function(function_name)


@app.command()
def logs(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to read logs from",
    ),
) -> None:
    """Reads log from a deployed function"""
    read_logs(function_name)


@app.command()
def list(
    service: Optional[CloudServiceType] = typer.Option(
        None,
        help="Type of service you want to list resources from",
        autocompletion=CloudServiceType.all,
    ),
) -> None:
    """Lists functions deployed to a service on GCP"""
    raise NotImplementedError()
