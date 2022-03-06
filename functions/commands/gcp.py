from typing import Optional

import typer

from functions import cloud
from functions import logs
from functions import styles
from functions import user
from functions.cloud import deploy_function
from functions.config.files import FunctionRegistry
from functions.constants import CloudProvider
from functions.constants import CloudServiceType
from functions.core import FTyper
from functions.gcp.autocomplete import autocomplete_deployed_function
from functions.gcp.autocomplete import gcp_delete_autocomplete
from functions.gcp.autocomplete import gcp_deploy_autocomplete
from functions.gcp.callbacks import check_if_function_can_be_deployed
from functions.gcp.callbacks import check_if_function_name_in_registry
from functions.gcp.cloud_function.cli import delete_function

app = FTyper(help="Interact with GCP functions.")


@app.command(disable=True)
def install() -> None:
    """Install required libraries"""
    raise NotImplementedError()


@app.command(disable=True)
def login() -> None:
    """Install required libraries"""
    raise NotImplementedError()


@app.command()
def deploy(
    function_name: str = typer.Argument(
        ...,
        help="The name of the function to deploy",
        autocompletion=gcp_deploy_autocomplete,
        callback=check_if_function_can_be_deployed,
    ),
) -> None:
    """
    Deploy a function in GCP.
    """
    function = FunctionRegistry.fetch_function(function_name)

    if function.status.GCP.is_deployed:
        user.confirm_abort(
            f"Function '{function_name}' is already deployed. Do you want to continue?"
        )

    deploy_function(function, provider=CloudProvider.GCP)

    user.inform(f"'{function_name}' functions has been deployed to GCP!")


@app.command()
def delete(
    function_name: str = typer.Argument(
        ...,
        help="The name of the function to delete",
        autocompletion=gcp_delete_autocomplete,
        callback=check_if_function_name_in_registry,
    ),
) -> None:
    """
    Deletes resources associated with a function in GCP.
    """
    provider = CloudProvider.GCP.upper()

    user.confirm_abort(
        f"Are you sure you want to remove '{function_name}' from {provider}?"
    )
    delete_function(function_name)
    user.inform(f"'{styles.green(function_name)}' has been removed from {provider}!")


@app.command()
def describe(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function in registry",
        autocompletion=autocomplete_deployed_function,
        callback=check_if_function_name_in_registry,
    ),
) -> None:
    """
    Shows information about a function deployed in GCP.
    """
    logs.debug(f"Fetching information about '{function_name}'")
    function = FunctionRegistry.fetch_function(function_name)
    cloud.describe_function(function, provider=CloudProvider.GCP)
    logs.debug(f"Describe command for '{function_name}' has executed")


@app.command("logs")
def fetch_logs(
    function_name: str = typer.Argument(
        ...,
        help="Name of the function in registry",
        autocompletion=autocomplete_deployed_function,
        callback=check_if_function_name_in_registry,
    ),
) -> None:
    """
    Show logs of a function deployed to GCP.
    """
    logs.debug(f"Fetching logs for '{function_name}'")
    cloud.read_logs(function_name, provider=CloudProvider.GCP)
    logs.debug(f"Logs command for '{function_name}' has executed")


@app.command()
def list(
    service: Optional[CloudServiceType] = typer.Option(
        CloudServiceType.CLOUD_FUNCTION,
        help="Type of service to list",
        autocompletion=CloudServiceType.all,
    ),
) -> None:
    """
    List functions deployed to a service in GCP
    """
    logs.debug(f"Fetching list of functions from {service}")
    cloud.list_functions(service=service, provider=CloudProvider.GCP)
    logs.debug(f"List command for {service} has been executed")
