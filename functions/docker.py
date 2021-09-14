from typing import List, Optional

import docker
from docker.models.images import Image as DockerImage
from docker.models.containers import Container as DockerContainer
from pydantic import ValidationError

from functions.types import FunctionConfig
from functions.system import load_config
from functions.errors import FunctionsError


# TODO: Find a better way of doing this
docker_client: docker.client = None
if not docker_client:
    docker_client = docker.from_env()


class DockerLabel:
    CONFIG: str = "package.functions.config_path"
    ORGANISATION: str = "package.functions.organisation"
    TAG: str = "package.functions.tag"


def get_config_from_image(image: DockerImage) -> FunctionConfig:
    config_path = image.labels.get(DockerLabel.CONFIG)
    try:
        return load_config(config_path)
    except ValidationError as error:
        raise FunctionsError(
            "Could not load image configuration. Missing config file. Try rebuilding an image"
        )


def get_function_tag_from_labels(labels: dict) -> Optional[str]:
    return labels.get(DockerLabel.TAG)


def all_images() -> List[DockerImage]:
    """Returns all functions created by this package"""
    return docker_client.images.list(
        filters={"label": f"{DockerLabel.ORGANISATION}=Ventress"}
    )


def all_functions() -> List[str]:
    """Returns the names of functions that are workable"""
    functions = []
    for image in all_images():
        function_tag = get_function_tag_from_labels(image.labels)
        if function_tag:
            functions.append(function_tag)
    return functions


def all_running_containers() -> List[DockerContainer]:
    """Returns all containers"""
    return docker_client.containers.list(
        filters={"label": f"{DockerLabel.ORGANISATION}=Ventress"}
    )


def all_running_functions() -> List[str]:
    """Returns a list of all running functions"""
    functions = []
    for container in all_running_containers():
        function_tag = get_function_tag_from_labels(container.labels)
        if function_tag:
            functions.append(function_tag)
    return functions

def build_image(image_name: str) -> DockerImage:
    ...

def remove_image(image_name: str):
    docker_client.images.remove(image_name)