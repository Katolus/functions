from typing import Optional

import typer

from functions import cloud
from functions import user
from functions.cloud import deploy_function
from functions.config.files import FunctionRegistry
from functions.constants import CloudProvider
from functions.constants import CloudServiceType
from functions.gcp.callbacks import gcp_logs_callback
from functions.gcp.cloud_function.cli import delete_function

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
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to deploy",
    ),
    service: Optional[CloudServiceType] = typer.Option(
        None,
        help="Type of service you want this resource to be deploy to",
        autocompletion=CloudServiceType.all,
    ),
) -> None:
    """Deploy a functions to GCP"""
    function = FunctionRegistry.fetch_function(function_name)

    deploy_function(function, provider=CloudProvider.GCP)

    user.inform(f"{function_name} functions has been deployed to GCP!")


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
    raise NotImplementedError


@app.command()
def logs(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function you want to read logs from",
        callback=gcp_logs_callback,
    ),
) -> None:
    """Reads log from a deployed function"""
    cloud.read_logs(function_name, provider=CloudProvider.GCP)


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
