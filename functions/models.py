"""Core function models"""

import shutil
from typing import Optional

from functions import logs
from functions.config.files import FunctionRegistry
from functions.config.models import FunctionConfig
from functions.config.models import FunctionRecord
from functions.constants import LocalStatus
from functions.docker.api import DockerContainer
from functions.docker.api import DockerImage
from functions.errors import ErrorRemovingResources
from functions.errors import FunctionContainerNotFoundError
from functions.errors import FunctionImageNotFoundError
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
    def image(self) -> Optional[DockerImage]:
        """
        Returns the image of the function if it exists.
        """
        if not self._image:
            try:
                self._image = DockerImage.get(self.name)
            except FunctionImageNotFoundError:
                logs.debug(f"Image for function {self.name} not found")

        return self._image

    @property
    def container(self) -> Optional[DockerContainer]:
        """
        Returns the container of the function.
        """
        if not self._container:
            try:
                self._container = DockerContainer.get(self.name)
            except FunctionContainerNotFoundError:
                logs.debug(f"Container for function {self.name} not found")
        return self._container

    def is_source_valid(self) -> bool:
        """
        Checks if the function's source is valid
        """
        return self.config.validate_source()

    def build(self, show_logs: bool = False) -> None:
        """
        Builds the function's image.
        """
        self._image = DockerImage.build(self._record, show_logs)

        # Set built status
        self._record.set_local_status(LocalStatus.BUILT)
        self._record.update_registry()

    def run(self) -> None:
        """
        Run the function locally
        """
        self._container = DockerContainer.run(self.image, self.name, self.config)
        # Set running status
        self._record.set_local_status(LocalStatus.RUNNING)
        self._record.update_registry()

    def stop(self) -> None:
        """
        Stop a function running locally
        """
        if container := self.container:
            container.stop()
            # Set stopped status
            self._record.set_local_status(LocalStatus.STOPPED)
            self._record.update_registry()
        else:
            raise FunctionNotRunningError(name=self.name)

    def remove(self) -> None:
        """
        Removes the function's image
        """
        if self.image:
            self.image.remove()

        # Set removed status
        self._record.set_local_status(LocalStatus.REMOVED)
        self._record.update_registry()

    def delete_all(self) -> None:
        """
        Deletes all the function's resources
        """
        # Stop the container from running
        if self.container:
            self.container.stop()
        # Remove the image of the function
        if self.image:
            self.image.remove()

        # Remvoe from the registry
        FunctionRegistry.remove_function(self.name)

    def delete_resources(self) -> None:
        """
        Deletes the function's resources
        """
        path = self.config.path
        try:
            shutil.rmtree(path, ignore_errors=False)
            logs.debug(f"Directory {path} has been removed successfully")
        except OSError as e:
            logs.exception(e)
            raise ErrorRemovingResources(error=e, name=self.name, path=path)
