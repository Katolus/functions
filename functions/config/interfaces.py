"""Holds interfaces specific to the config module"""
from __future__ import annotations

import functools
from typing import Any, ClassVar, Dict, Mapping, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Protocol
else:
    # < Python 3.7.2
    # Consider using typing_extensions for this
    # Or maybe assign an ABC class instead if not available
    Protocol = object

import toml

from functions.system import construct_filepath_in_config_dir


class File(Protocol):
    """Interface for working with system files in config directory"""

    DEFAULT_FILENAME: ClassVar[str]

    @classmethod
    @functools.lru_cache()
    def filepath(cls) -> str:
        """Returns filepath"""

        return construct_filepath_in_config_dir(cls.DEFAULT_FILENAME)

    @classmethod
    def create(cls) -> None:
        """Creates the file with default content"""

        cls.write_to_file(cls.default_content())

    @classmethod
    def default_content(cls) -> File:
        """Returns the default content for the file"""

        return cls()

    @classmethod
    def write_to_file(cls, content: Any) -> None:
        """Writes the content into the file"""

        raise NotImplementedError

    @classmethod
    def load(cls) -> File:
        """Loads the file"""

        raise NotImplementedError


class TOML(Protocol):
    """Interface for TOML files"""

    @classmethod
    def from_toml(cls, filepath: str) -> Mapping:
        """Loads a .toml file"""

        return toml.load(filepath)

    @classmethod
    def to_toml(cls, config: Dict) -> str:
        """Returns content from a .toml file"""

        return toml.dumps(config)
