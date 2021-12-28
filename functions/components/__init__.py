from abc import ABC
from typing import List, Literal

ComponentType = Literal["docker", "gcp"]


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


def get_all_available_components() -> List[Component]:
    """
    Returns a list of all available components.
    """
    components = Component.__subclasses__()
    return [component for component in components if component.is_available()]