from typing import Dict

from functions import flows
from functions import logs
from functions import user
from functions.config.files import FunctionRegistry
from functions.constants import CloudStatus
from functions.core import FTyper
from functions.docker.api import DockerImage
from functions.gcp.cloud_function.cli import fetch_deployed_function_names

app = FTyper(help="Sync registry functions.")


@app.command()
def local() -> None:
    """
    Sync registry functions with Docker.
    """
    logs.debug("Syncing local functions")
    # Get the list of functions built or running locally from the the DockerManager
    images: Dict[str, str] = {}
    for image in DockerImage.get_all():
        images[image.name] = image.id
    image_names = images.keys()

    # Retrieve functions from the registry
    functions_names = FunctionRegistry.fetch_built_function_names()

    # Find the different names present in one list but not the other
    not_in_registry = list(set(image_names) - set(functions_names))
    logs.debug(f"Functions not in registry: {not_in_registry}")
    not_in_docker = list(set(functions_names) - set(image_names))
    logs.debug(f"Functions not in docker: {not_in_docker}")

    # Check functions in registry, but not in Docker
    for function_name in not_in_docker:
        user.inform(f"Function '{function_name}' is not built locally.")

    # Check functions in Docker, but not in registry
    for function_name in not_in_registry:
        user.inform(
            f"There is a Docker function({function_name}) image that does not match a record in the registry."
        )

        # Get the docker image
        image_id = images[function_name]
        image = DockerImage.get(image_id)

        # Check if the source of the image is still valid
        if image.is_source_valid():
            should_add = user.confirm(
                f"The source of the image {image.name} is still valid. "
                f"Do you want to add it the registry?."
            )

            if should_add:
                # Add the image's source code to the registry
                flows.add_function(image.config.path, False)
                continue

        else:
            # The source of the image is not valid anymore
            should_remove = user.confirm(
                f"The source of the image {image.name} is not valid anymore. "
                f"Do you want to remove the image?"
            )

            if should_remove:
                # Remove the image's source code from the registry
                image.remove()
                user.inform(f"Image {image.name} has been removed.")
                continue
    logs.debug("Syncing local functions finished...")


@app.command()
def gcp() -> None:
    """
    Sync registry functions with GCP.
    """
    logs.debug("Syncing GCP functions")
    # Get the list of functions deployed to GCP
    # ### Note ###
    # Will be an issue once services doing work for more
    # than just a cloud function will be used, but that
    # features needs to be properly reviewed before implemented furter
    # ### END ###
    deployed_functions = fetch_deployed_function_names()

    # Retrive functions that have status DEPLOYED
    functions_names = [
        function.name
        for function in FunctionRegistry.fetch_all_functions()
        if function.status.GCP == CloudStatus.DEPLOYED
    ]

    # Find the different names present in one list but not the other
    not_in_registry = list(set(deployed_functions) - set(functions_names))
    logs.debug(f"Functions not in registry: {not_in_registry}")
    not_in_deployed = list(set(functions_names) - set(deployed_functions))
    logs.debug(f"Functions not in deployed: {not_in_deployed}")

    if not_in_registry == [] and not_in_deployed == []:
        user.inform("Nothing to report. All functions are in sync 🔥")

    # Update with statuses of functions in not_in_deployed
    for function_name in not_in_deployed:
        function = FunctionRegistry.fetch_function(function_name)
        # Check if status is deployed to GCP
        if function.status.GCP != CloudStatus.DEPLOYED:
            logs.debug(
                f"Skiping function {function_name} since is not deployed to GCP."
            )
            continue

        # Notify use that the function status is mismatched
        user.inform(
            f"Function - '{function_name}' - GCP status is not sync. GCP({CloudStatus.UNKNOWN}) vs Registry({function.status.GCP})"
        )

        # Inform the user that function's status will be updated
        user.inform(
            f"Its GCP status will be updated to '{CloudStatus.UNKNOWN.upper()}'"
        )

        function.set_gcp_status(CloudStatus.UNKNOWN)
        function.update_registry()  # Not the most efficient way
        logs.debug(f"Function {function_name} has been updated.")

    # Inform user of functions deployed to GCP and matching registry requirements
    if not_in_registry != []:
        user.inform(
            f"There are several functions deployed to GCP that matches registry requirements, but are not present in this registry : {not_in_registry}"
        )
    logs.debug("Syncing GCP functions finished...")
