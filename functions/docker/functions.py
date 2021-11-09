"""Functional approach towards managing docker objects and processes"""

import json
import re
from typing import List

import docker
from docker.utils.json_stream import json_stream

from functions import logs
from functions import user
from functions.config.models import FunctionRecord
from functions.docker.enums import DockerLabel
from functions.docker.models import BuildVariables
from functions.docker.models import DockerContainer
from functions.docker.models import DockerImage
from functions.docker.types import DockerBuildAPIGenerator
from functions.errors import FunctionBuildError

client: docker.client.DockerClient = docker.from_env()


def _construct_build_variables(function: FunctionRecord) -> BuildVariables:
    """
    Constructs the build variables for the docker build process from a function
    """
    logs.debug(f"Constructing build variables for {function.name}")
    config = function.config
    return BuildVariables.parse_obj(
        {
            {
                "path": config.path,
                "tag": function.name,
                "buildargs": {
                    "TARGET": config.run_variables.entry_point,
                    "SOURCE": config.run_variables.source,
                    "SIGNATURE_TYPE": config.run_variables.signature_type,
                },
                "labels": {
                    DockerLabel.FUNCTION_NAME: function.name,
                    DockerLabel.FUNCTION_PATH: config.path,
                    DockerLabel.CONFIG_PATH: config.config_path,
                    DockerLabel.CONFIG: json.dumps(config.json()),
                    DockerLabel.ORGANISATION: "Ventress",
                },
            }
        }
    )


def _call_build_api(function: FunctionRecord) -> DockerBuildAPIGenerator:
    """
    Calls docker's build API and serves the output

    This function is not ideally asynchronous back to the console.
    Most likely due to to fact the request to the API does not release
    unless it makes an external call. Not sure, but I really don't want to
    spend more time making this work. Not benefit.
    """
    build_variables = _construct_build_variables(function)

    # Snippet copied and adjusted from the docker-py
    # package to account for stream logs as build takes place.
    resp = client.api.build(**build_variables.dict())
    result_stream = json_stream(resp)

    last_event = None
    image_id = None

    # TODO: Revisit this to check if the build stream needs to be split
    for chunk in result_stream:
        if "error" in chunk:
            raise FunctionBuildError(
                name=function.name, reason=chunk["error"], build_log=result_stream
            )
        if "stream" in chunk:
            match = re.search(
                r"(^Successfully built |sha256:)([0-9a-f]+)$", chunk["stream"]
            )
            if match:
                image_id = match.group(2)
        last_event = chunk
        yield image_id, last_event.get("stream")


def get_image(image_id: str) -> DockerImage:
    """
    Returns an image by id
    """
    return client.images.get(image_id)


def build_image(function: FunctionRecord, show_logs: bool) -> DockerImage:
    """
    Builds the image for the function
    """
    logs.debug(f"Building image for {function.name}")

    # TODO: Try to include this in
    image = None
    image_id = ""

    for image_id_chunk, log_chunk in _call_build_api(function):
        if show_logs and log_chunk and log_chunk != "\n":
            user.inform(log_chunk)

        if image_id_chunk:
            # If the chunk is present that means the build has
            # been successful and an id been render to output
            image = get_image(image_id)

    if not image:
        raise FunctionBuildError(
            name=function.name,
            reason="Could not retrieve image from the build logs",
            build_log=None,
        )

    logs.debug(f"Built image {image.id} for {function.name}")

    return image


def remove_image(image: DockerImage) -> None:
    """
    Removes an image
    """
    # TODO: Validate if this works
    logs.debug(f"Removing image {image.id}")
    image.remove()


def remove_image_by_name(name: str) -> None:
    """
    Removes an image by name
    """
    logs.debug(f"Removing image {name}")
    client.images.remove(name)


def get_container(name: str):
    """
    Returns a container by name
    """
    logs.debug(f"Getting container {name}")
    return client.containers.get(name)


def run_container(
    image: DockerImage,
    function: FunctionRecord,
) -> DockerContainer:
    """
    Runs a container from an image
    """
    logs.debug(f"Running container for {function.name}")

    return client.containers.run(
        image,
        ports={"8080": function.config.run_variables.port},
        remove=True,
        name=function.config.run_variables.name,
        detach=True,
    )


def stop_container(container: DockerContainer) -> None:
    """
    Stops a container
    """
    logs.debug(f"Stopping container {container.name}")
    container.stop()


def get_containers(self) -> List:
    """
    Returns a list of all the containers
    """
    # TODO: Validate this works
    return client.containers.list()
