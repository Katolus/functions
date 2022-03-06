"""Holds protocol classes that other classes across the package can use from"""
from typing import ClassVar, TYPE_CHECKING

from functions import logs
from functions.config.models import FunctionConfig
from functions.config.models import FunctionRecord
from functions.constants import RequiredFile
from functions.system import add_file
from functions.system import make_dir
from functions.types import PathStr

if TYPE_CHECKING:
    from typing import Protocol
else:
    # < Python 3.7.2
    # Consider using typing_extensions for this
    # Or maybe assign an ABC class instead if not available
    # More research needed on the differences between ABC and Protocols
    Protocol = object


class Default(Protocol):
    """
    Protocol for default classes.

    That is classes which implement a models of generating default variables, files etc...
    for a function type like the Cloud Functions.
    """

    DEFAULT_PORT: ClassVar[int]

    @classmethod
    def config(cls, f_name: str, f_dir: PathStr) -> FunctionConfig:
        """
        Generates a default configuration for a given function type.
        """
        raise NotImplementedError

    @classmethod
    def generate_required_files(cls, function: FunctionRecord) -> None:
        """
        Generates all required files for a given function type.
        """
        logs.debug(f"Generating required files for PubSub function: {function.name}")

        f_dir = function.config.path
        # Make the function directory
        make_dir(f_dir)
        # Add a Dockerfile
        cls.generate_dockerfile(function)

        # Add a requirements.txt
        cls.generate_requirements(function)

        # Add a .dockerignore
        cls.generate_dockeringore(function)

        # Add a an entry point script
        cls.generate_entry_point(function)

    @classmethod
    def generate_dockerfile(cls, function: FunctionRecord) -> None:
        """
        Generates a Dockerfile for a given function type.
        """
        raise NotImplementedError

    @classmethod
    def generate_entry_point(cls, function: FunctionRecord) -> None:
        """
        Generates an entry point script for a given function type.
        """
        raise NotImplementedError

    @classmethod
    def generate_dockeringore(cls, function: FunctionRecord) -> None:
        """
        Generates a .dockerignore for a given function type.
        """
        content = """
# Python
.mypy_cache

# Docker specific
Dockerfile
.dockerignore

# Configuration
config.json
        """
        add_file(function.config.path, RequiredFile.DOCKERIGNORE, content)

    @classmethod
    def generate_requirements(cls, function: FunctionRecord) -> None:
        """
        Generates a requirements.txt for a given function type.
        """
        content = """"""
        add_file(function.config.path, RequiredFile.REQUIREMENTS, content)
