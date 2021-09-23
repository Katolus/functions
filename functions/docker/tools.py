"""Set of functions meant for building, manipulating docker objects."""

from functions.docker.classes import DockerImage
from functions.docker.client import docker_client


def build_image(image_name: str) -> DockerImage:
    # TODO: Export inline code
    ...


def remove_image(image_name: str):
    docker_client.images.remove(image_name)
