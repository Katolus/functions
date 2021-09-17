from typing import Optional
from functions.constants import CloudServiceType
from pathlib import Path

import typer

from functions.autocomplete import autocomplete_deploy_functions
from functions.input import confirm_abort
from functions.gcp import delete_function
from functions.gcp import deploy_function
from functions.system import load_config


app = typer.Typer(help="Deploy functions in GCP")


@app.command()
def install():
    """Install required libraries"""
    raise NotImplementedError()


@app.command()
def update():
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
    # TODO: Make service an enum
    service: Optional[CloudServiceType] = typer.Option(
        None,
        help="Type of service you want this resource to be deploy to",
        autocompletion=CloudServiceType.all,
    ),
):
    """Deploy a functions to GCP"""
    config = load_config(function_dir)
    service_type = service or config.deploy_variables.service

    deploy_function(config, CloudServiceType(service_type))

    typer.echo(f"{config.run_variables.name} functions has been deployed to GCP!")


@app.command()
def delete(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to remove",
    ),
):
    """Deletes a functions deployed to GCP"""
    # Check if the functions is really deployed. Add to confirmation.
    # TODO: Implement a delete option with a confirmation
    confirm_abort(f"Are you sure you want to remove '{function_name}'?")
    delete_function(function_name)


@app.command()
def describe():
    """Returns information about a deployed function"""
    raise NotImplementedError()


@app.command()
def logs():
    """Reads log from a deployed function"""
    raise NotImplementedError()
