from abc import ABC
from enum import Enum
from typing import List, Literal, Type

from functions import logs


class ComponentEnum(str, Enum):
    """
    Enum for all available components.
    """

    DOCKER = "docker"
    GCP = "gcp"


ComponentType = Literal[ComponentEnum.DOCKER, ComponentEnum.GCP]


class Component(ABC):
    """
    Base class for all components.
    """

    NAME: str
    DESCRIPTION: str
    TYPE: ComponentType

    @classmethod
    def is_available(cls) -> bool:
        """
        Returns True if the component is available for the current platform.
        """
        raise NotImplementedError()

    @classmethod
    def is_installed(cls) -> bool:
        """
        Returns True if the component is installed on the current platform.
        """
        raise NotImplementedError()

    @classmethod
    def install(cls) -> None:
        """
        Installs the component on the current platform.
        """
        raise NotImplementedError()

    @classmethod
    def show_instruction(cls) -> None:
        """
        Prints the instructions for installing the component.
        """
        raise NotImplementedError()


def get_all_available_components() -> List[Type[Component]]:
    """
    Returns a list of all available components.
    """
    components = Component.__subclasses__()
    logs.debug(f"Available components: {components}")
    return [component for component in components if component.is_available()]
