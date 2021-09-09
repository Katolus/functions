from typing import List

import docker
from docker.models.images import Image as DockerImage

from functions.hints import Config
from functions.errors import FunctionsError


docker_client: docker.client = None
if not docker_client:
    docker_client = docker.from_env()


class DockerLabel:
    CONFIG: str = "package.functions.config_path"
    ORGANISATION: str = "package.functions.organisation"
    TAG: str = "package.functions.tag"


def get_config_from_image(image: DockerImage) -> Config:
    config_path = image.labels.get(DockerLabel.CONFIG)
    try:
        return load_config(config_path)
    except ValidationError as error:
        raise FunctionsError(
            "Could not load image configuration. Missing config file. Try rebuilding an image"
        )


def all_functions() -> List[DockerImage]:
    images = docker_client.images.list(
        filters={"label": f"{DockerLabel.ORGANISATION}=Ventress"}
    )
    return images