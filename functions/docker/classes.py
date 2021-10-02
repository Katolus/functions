from typing import Any, Generic, Optional, TypeVar, Union

import docker
from docker.models.images import Image
from docker.models.containers import Container
from pydantic import BaseModel
from pydantic import PrivateAttr


# TODO: Find a way to make them a pydantic class

# DockerImage = Generic[DockerImageType]

DockerImageType = TypeVar("DockerImageType", bound=Image)


# PIOTR
# I think this needs docker py stubs first before anything I can make it work with pydantic
class DockerImage(Generic[DockerImageType]):
    ...


class DockerContainer(Container):
    ...


class DockerFunction(BaseModel):
    """Base class for representing docker functions."""

    _image: Optional[Image] = PrivateAttr()
    _container: Optional[Container] = PrivateAttr()
    name: str
    image: Optional[DockerImage]  # Temp solution
    container: Optional[DockerContainer]  # Temp solution

    def __init__(
        self, image: Image = None, container: Container = None, **data: Any
    ) -> None:
        super().__init__(**data)
        self._image = image
        self._container = container

    @property
    def status(self) -> str:
        """Returns a status of a docker function."""
        status = "Unknown"
        if self.image:
            status = "Build"
        if self.container:
            status = "Running"
        return status

    class Config:
        arbitrary_types_allowed = True
