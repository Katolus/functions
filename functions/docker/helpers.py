from functions.constants import DockerLabel
from typing import Optional
from typing import List
from functions.config import FunctionConfig
from functions.system import load_config

# Add stubs for docker-py
from functions.docker.client import docker_client
from functions.docker.classes import DockerContainer
from functions.docker.classes import DockerFunction
from functions.docker.classes import DockerImage


def get_config_from_image(image: DockerImage) -> FunctionConfig:
    """Returns a function config from a given function image"""
    config_path = image.labels.get(DockerLabel.FUNCTION_PATH)
    return load_config(config_path)


def get_function_name_from_labels(labels: dict) -> Optional[str]:
    """Returns a function name from docker labels"""
    return labels.get(DockerLabel.FUNCTION_NAME)


def all_images() -> List[DockerImage]:
    """Returns all functions created by this package"""
    return docker_client.images.list(
        filters={"label": f"{DockerLabel.ORGANISATION}=Ventress"}
    )


def all_functions() -> List[DockerFunction]:
    """Returns the names of functions that are workable"""
    functions = []
    for image in all_images():
        function_name = get_function_name_from_labels(image.labels)
        if function_name:
            function = DockerFunction(name=function_name, image=image)
            functions.append(function)
    return functions


def all_running_containers() -> List[DockerContainer]:
    """Returns all containers"""
    return docker_client.containers.list(
        filters={"label": f"{DockerLabel.ORGANISATION}=Ventress"}
    )


def all_running_functions() -> List[DockerFunction]:
    """Returns a list of all running functions"""
    functions = []
    for container in all_running_containers():
        function_name = get_function_name_from_labels(container.labels)
        if function_name:
            function = DockerFunction(name=function_name, container=container)
            functions.append(function)
    return functions
