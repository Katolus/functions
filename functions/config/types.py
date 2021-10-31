import functools
from typing import Dict, Mapping, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Protocol
else:
    # Consider using typing_extensions for this
    # Or maybe assign an ABC class instead if not available
    Protocol = object

import toml

from functions.config.helpers import construct_filepath_in_config
from functions.system import check_if_file_exists


class File(Protocol):
    DEFAULT_CONFIG_FILENAME: str  # Make this a class attribute

    @classmethod
    def initialize_file(cls) -> None:
        """Initializes the file"""
        if check_if_file_exists(cls.filepath()):
            cls.load()
        else:
            cls.create()

    @classmethod
    @functools.lru_cache()
    def filepath(cls) -> str:
        """Returns filepath"""
        return construct_filepath_in_config(cls.DEFAULT_CONFIG_FILENAME)

    @classmethod
    def create(cls) -> None:
        """Creates the file with default content"""
        cls.write_to_file(cls.default_content())

    @classmethod
    def default_content(cls) -> "File":
        """Returns the default content for the file"""
        raise cls()

    @classmethod
    def write_to_file(cls, content: "File") -> None:
        """Writes the content into the file"""
        raise NotImplementedError

    @classmethod
    def load(cls) -> "File":
        """Loads the file"""
        raise NotImplementedError


class TOML(Protocol):
    @classmethod
    def from_toml(cls, filepath: str) -> Mapping:
        """
        Loads a .toml file.
        """
        return toml.load(filepath)

    @classmethod
    def to_toml(cls, config: Dict) -> str:
        """
        Returns content from a .toml file.
        """
        return toml.dumps(config)
