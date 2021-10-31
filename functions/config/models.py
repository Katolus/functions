from pydantic import BaseModel

from functions.config.types import File
from functions.config.types import TOML
from functions.system import write_to_file


class AppConfig(BaseModel, File, TOML):
    """
    This class is used to represent the main configuration file.
    """

    DEFAULT_CONFIG_FILENAME: str = "config.toml"

    @classmethod
    def write_to_file(cls, content: "AppConfig") -> None:
        """Writes a config content to the config file"""
        write_to_file(cls.filepath(), cls.to_toml(content.dict()))

    @classmethod
    def load(cls) -> "AppConfig":
        """
        Loads the main configuration from file.
        """
        filepath = cls.filepath()
        return cls.parse_obj(cls.from_toml(filepath))
