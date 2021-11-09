"""Core function models"""

from typing import Optional

from functions.config.files import FunctionRegistry
from functions.config.models import FunctionConfig
from functions.config.models import FunctionRecord
from functions.constants import LocalStatus
from functions.docker.api import DockerContainer
from functions.docker.api import DockerImage
from functions.errors import FunctionNotRunningError


class Function:
    """Function class"""

    _image: Optional[DockerImage] = None
    _container: Optional[DockerContainer] = None
    _record: FunctionRecord

    def __init__(self, name: str) -> None:
        # Throw an error if the function is not registered
        self._record = FunctionRegistry.fetch_function(name)

    @property
    def name(self) -> str:
        return self._record.name

    @property
    def config(self) -> FunctionConfig:
        return self._record.config

    @property
    def image(self) -> DockerImage:
        """
        Returns the image of the function.
        """
        if not self._image:
            self._image = DockerImage.get(self.name)
        return self._image

    @property
    def container(self) -> Optional[DockerContainer]:
        """
        Returns the container of the function.
        """
        if not self._container:
            self._container = DockerContainer.get(self.name)
        return self._container

    def run(self) -> None:
        """
        Run the function locally
        """
        self._container = DockerContainer.run(
            self.image, self.name, self.config.run_variables.port
        )
        # Set running status
        self._record.set_local_status(LocalStatus.RUNNING)

    def stop(self) -> None:
        """
        Stop a function running locally
        """
        if container := self.container:
            container.stop()
            # Set stopped status
            self._record.set_local_status(LocalStatus.STOPPED)
        else:
            raise FunctionNotRunningError(name=self.name)
