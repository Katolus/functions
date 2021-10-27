"""Set of functions meant for building, manipulating docker objects."""
import json
import re
from typing import Generator, Optional
from typing import Dict, Generator, Tuple

import docker
import typer
from docker.utils.json_stream import json_stream
from pydantic.main import BaseModel

from functions.config import FunctionConfig
from functions.constants import DockerLabel
from functions.docker.classes import DockerContainer, DockerImage
from functions.docker.client import docker_client
from functions.errors import FunctionBuildError


class BuildArgs(BaseModel):
    TARGET: str
    SOURCE: str
    SIGNATURE_TYPE: str


class BuildVariables(BaseModel):
    path: str
    tag: str
    buildargs: BuildArgs
    labels: Dict[DockerLabel, str]


def construct_build_variables(config: FunctionConfig) -> BuildVariables:
    """Constructs build variables for a docker build process"""
    function_name = config.run_variables.name

    return BuildVariables(
        **{
            "path": config.path,
            "tag": function_name,
            "buildargs": {
                "TARGET": config.run_variables.entry_point,
                "SOURCE": config.run_variables.source,
                "SIGNATURE_TYPE": config.run_variables.signature_type,
            },
            "labels": {
                DockerLabel.FUNCTION_NAME: function_name,
                DockerLabel.FUNCTION_PATH: config.path,
                DockerLabel.CONFIG_PATH: config.config_path,
                DockerLabel.CONFIG: json.dumps(config.json()),
                DockerLabel.ORGANISATION: "Ventress",
            },
        }
    )


DockerBuildAPIGenerator = Generator[Tuple[Optional[str], Optional[str]], None, None]


def call_build_api(build_variables: BuildVariables) -> DockerBuildAPIGenerator:
    """
    Calls docker's build API and serves the output

    This function is not ideally asynchronous back to the console.
    Most likely due to to fact the request to the API does not release
    unless it makes an external call. Not sure, but I really don't want to
    spend more time making this work. Not benefit.
    """
    # Snippet copied and adjusted from the docker-py
    # package to account for stream logs as build takes place.
    resp = docker_client.api.build(**build_variables.dict())
    result_stream = json_stream(resp)

    last_event = None
    image_id = None

    for chunk in result_stream:
        if "error" in chunk:
            raise docker.errors.BuildError(chunk["error"], result_stream)
        if "stream" in chunk:
            match = re.search(
                r"(^Successfully built |sha256:)([0-9a-f]+)$", chunk["stream"]
            )
            if match:
                image_id = match.group(2)
        last_event = chunk
        yield image_id, last_event.get("stream")


def build_image(config: FunctionConfig, show_logs: bool) -> DockerImage:
    """Builds a function as a docker image"""
    build_variables = construct_build_variables(config)

    image = None
    image_id = ""

    try:
        build_generator = call_build_api(build_variables)

        for image_id_chunk, log_chunk in build_generator:
            if show_logs and log_chunk != "\n":
                typer.echo(log_chunk)

            if image_id_chunk:
                # If the chunk is present that means the build has
                # been successful and an id been render to output
                image_id = image_id_chunk

    except docker.errors.BuildError as error:
        # Consider adding the error to the output of an error
        raise FunctionBuildError(error=error)

    image = get_image(image_id)

    return image


def get_image(image_id: str) -> DockerImage:
    """Returns a docker image object"""
    return docker_client.images.get(image_id)


def remove_image(image_name: str) -> None:
    """Removes a docker image"""
    docker_client.images.remove(image_name)


def run_container(
    function_image: DockerImage, config: FunctionConfig
) -> DockerContainer:
    """Runs a container of a function"""
    container = docker_client.containers.run(
        function_image,
        ports={"8080": config.run_variables.port},
        remove=True,
        name=config.run_variables.name,
        detach=True,
    )

    return container


def stop_container(function_name: str) -> DockerContainer:
    """Stops a docker container"""
    container = docker_client.containers.get(function_name)
    container.stop()
    return container
