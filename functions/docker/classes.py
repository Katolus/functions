from typing import Any, Dict, Generic, Optional, TypeVar

from docker.models.containers import Container
from docker.models.images import Image
from pydantic import BaseModel
from pydantic import PrivateAttr

from functions.config.models import FunctionConfig
from functions.constants import DockerLabel
from functions.constants import LocalStatus

DockerImageType = TypeVar("DockerImageType", bound=Image)


class DockerImage(BaseModel, Generic[DockerImageType]):
    labels: Dict[Any, str]

    @property
    def config(self) -> FunctionConfig:
        config_path = self.labels.get(DockerLabel.FUNCTION_PATH)
        return FunctionConfig.load(config_path)


class DockerContainer(BaseModel, Container):
    @property
    def config(self) -> FunctionConfig:
        raise NotImplementedError()


class DockerFunction(BaseModel):
    """Base class for representing docker functions."""

    _image: Optional[Image] = PrivateAttr()
    _container: Optional[Container] = PrivateAttr()
    name: str
    image: Optional[DockerImage]
    container: Optional[DockerContainer]

    def __init__(
        self, image: Image = None, container: Container = None, **data: Any
    ) -> None:
        super().__init__(**data)
        self._image = image
        self._container = container
        if self._image:
            self.image = DockerImage(labels=self._image.labels)
        if self._container:
            self.container = DockerContainer.parse_obj(self._container.__dict__)

    @property
    def status(self) -> str:
        """Returns a status of a docker function."""
        status = LocalStatus.UNKNOWN
        if self.image:
            status = LocalStatus.BUILT
        if self.container:
            status = LocalStatus.RUNNING
        return status

    @property
    def config(self) -> Optional[FunctionConfig]:
        # Probably worth throwing an error here
        config_source = self.image or self.container
        return config_source.config if config_source else None

    class Config:
        arbitrary_types_allowed = True
