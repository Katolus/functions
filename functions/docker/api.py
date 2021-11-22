"""Functional approach towards managing docker objects and processes"""
from __future__ import annotations

import json
import re
from typing import List

import docker
from docker.models.containers import Container
from docker.models.images import Image
from docker.utils.json_stream import json_stream

from functions import logs
from functions import user
from functions.config.models import FunctionRecord
from functions.docker.enums import DockerLabel
from functions.docker.helpers import get_function_name_from_labels
from functions.docker.models import BuildVariables
from functions.docker.types import DockerBuildAPIGenerator
from functions.docker.types import DockerLabelsDict
from functions.errors import FunctionBuildError
from functions.errors import FunctionImageNotFoundError

client: docker.client.DockerClient = docker.from_env()


def _construct_build_variables(function: FunctionRecord) -> BuildVariables:
    """
    Constructs the build variables for the docker build process from a function
    """
    logs.debug(f"Constructing build variables for {function.name}")
    config = function.config
    return BuildVariables.parse_obj(
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

    # There is a way to push results in to another stream and return for things like logs
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


def get_image(image_id: str) -> Image:
    """
    Returns an image by id.
    """
    try:
        # Takes in both the function's name and the image id.
        return client.images.get(image_id)
    except docker.errors.ImageNotFound:
        raise FunctionImageNotFoundError(image_id=image_id)


def build_image(function: FunctionRecord, show_logs: bool) -> Image:
    """
    Builds the image for the function
    """
    logs.debug(f"Building image for {function.name}")

    image = None

    for image_id_chunk, log_chunk in _call_build_api(function):
        if show_logs and log_chunk and log_chunk != "\n":
            user.inform(log_chunk)

        if image_id_chunk:
            # If the chunk is present that means the build has
            # been successful and an id been render to output
            image = get_image(image_id_chunk)

    if not image:
        raise FunctionBuildError(
            name=function.name,
            reason="Could not retrieve image from the build logs",
            build_log=None,
        )

    logs.debug(f"Built image {image.id} for the '{function.name}' function")

    return image


def remove_image_by_name(name: str) -> None:
    """
    Removes an image by name
    """
    logs.debug(f"Removing image {name}")
    client.images.remove(name)  # type: ignore


def get_container(name: str) -> Container:
    """
    Returns a container by name
    """
    logs.debug(f"Getting container {name}")
    return client.containers.get(name)


def run_container(
    image: Image,
    function_name: str,
    port: int,
) -> Container:
    """
    Runs a container from an image
    """
    logs.debug(f"Running container for {function_name}")

    return client.containers.run(
        image,
        ports={"8080": port},
        remove=True,
        name=function_name,
        detach=True,
    )


def stop_container(name: str) -> None:
    """
    Stops a container
    """
    container = get_container(name)
    logs.debug(f"Stopping container {name}")
    container.stop()  # type: ignore


def get_all_images() -> List[Image]:
    """Returns all functions created by this package"""
    return client.images.list(filters={"label": f"{DockerLabel.ORGANISATION}=Ventress"})


class DockerImage:
    """
    A wrapper class around the docker Image class.
    """

    _image: Image

    def __init__(self, image: Image, /) -> None:
        self._image = image

    @property
    def id(self) -> str:
        return self._image.id

    @property
    def name(self) -> str:
        return get_function_name_from_labels(self._image.labels)

    @property
    def labels(self) -> DockerLabelsDict:
        return self._image.labels

    def remove(self) -> None:
        """
        Remove the image from the docker daemon.
        """
        remove_image_by_name(self._image.id)

    @classmethod
    def build(cls, function: FunctionRecord, show_logs: bool = False) -> DockerImage:
        """
        Builds the image
        """

        return cls(build_image(function, show_logs))

    @classmethod
    def get(cls, image_id: str) -> DockerImage:
        """
        Get an image from the docker daemon.
        """
        # `image_id` can be either the image name or the image id.
        return cls(get_image(image_id))

    @classmethod
    def get_all(cls) -> List[DockerImage]:
        """
        Returns all the images
        """
        return [cls(image) for image in get_all_images()]

    @classmethod
    def get_all_names(cls) -> List[str]:
        """
        Return a list of all the image names
        """
        return [image.name for image in cls.get_all()]


class DockerContainer:
    """
    A wrapper class around the docker Container class.
    """

    _container: Container

    def __init__(self, container: Container, /) -> None:
        self._container = container

    def stop(self) -> None:
        """Stops a running container"""
        stop_container(self._container.id)

    @classmethod
    def run(cls, image: DockerImage, name: str, port: int) -> DockerContainer:
        """
        Run the container.
        """
        container = run_container(image._image, name, port)
        return cls(container)

    @classmethod
    def get(cls, container_id: str) -> DockerContainer:
        """
        Get a container from the docker daemon.
        """
        return cls(get_container(container_id))
