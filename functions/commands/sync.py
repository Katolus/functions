import typer

from functions import logs

app = typer.Typer(help="Sync components")


@app.command()
def local() -> None:
    """Syncs the state of locally built functions"""
    logs.debug("Syncing local functions")
    # Get the list of functions built or running locally from the the DockerManager

    # Retrieve functions from the registry

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
