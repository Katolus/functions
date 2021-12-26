import typer

from functions import logs
from functions.config.files import FunctionRegistry
from functions.docker.api import DockerImage

app = typer.Typer(help="Sync components with the registry")


@app.command()
def local() -> None:
    """Syncs the state of locally built functions"""
    logs.debug("Syncing local functions")
    # Get the list of functions built or running locally from the the DockerManager
    images = DockerImage.get_all_names()
    print(images)
    # Retrieve functions from the registry
    function_names = FunctionRegistry.fetch_built_function_names()
    print(function_names)
    # Compare the two lists and sync the state of the functions

    # Save the results to the registry

    # Report the results to the user


@app.command()
def gcp() -> None:
    """Syncs the state of GCP functions"""
    logs.debug("Syncing GCP functions")
    # Get the list of functions deployed to GCP

    # Retrive functions from the registry

    # Compare the two lists and sync the functions

    # Save the results to the registry

    # Report the results to the user
