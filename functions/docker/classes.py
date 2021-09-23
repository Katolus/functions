from typing import Optional, Union

import docker
from docker.models.images import Image
from docker.models.containers import Container
from pydantic import BaseModel


# TODO: Find a way to make them a pydantic class
class DockerImage(Image):
    ...


class DockerContainer(Container):
    ...
    

class DockerFunction(BaseModel):
    """Base class for representing docker functions."""

    name: str
    image: Optional[Union[DockerImage, Image]] # Temp solution
    container: Optional[Union[DockerContainer, Image]] # Temp solution

    def status(self) -> str:
        """Returns a status of a docker function."""
        return "self.image"

    class Config:
        arbitrary_types_allowed = True