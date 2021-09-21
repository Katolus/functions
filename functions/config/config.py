"""Stores logic around creating and using a configuration file to amend and enhance the functioning of the package."""
import os
from pathlib import Path
from typing import Any

import toml
from pydantic import BaseModel

BASE_DIR_NAME = "ventress-functions"


class AppConfigManager(BaseModel):
    """Represents the configuration file for the package"""

    _base_dir: str = BASE_DIR_NAME
    _config_source: str = "config.toml"
    history_file: str = ""
    functions_file: str = ""
    default_region: str = ""

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._make_base_dir()
        if self.config_exists:
            self.read()
        else:
            self.create(self.config_path)
        self.save()

    def _make_base_dir(self):
        """Create the base directory for the configurations to be stored"""
        # Only on Posix
        os.makedirs(self.base_dir, exist_ok=True)

    def _write(self, file_path: str, content: str):
        with open(file_path, "w") as file:
            file.write(content)

    @property
    def base_dir(self) -> str:
        """Path to the configuration directory."""
        return os.path.join(self.config_home_path, self._base_dir)

    @property
    def config_home_path(self) -> str:
        """Returns the configuration folder"""
        config_folder = ".config"
        return os.path.join(Path().home(), config_folder)

    @property
    def config_path(self) -> str:
        """Returns the path to the configuration file."""
        return os.path.join(self.base_dir, self._config_source)

    @property
    def config_exists(self) -> bool:
        return Path(self.config_path).exists()

    def create(self, file_path: str):
        """Create the configuration file if it does not exist."""

        if Path(file_path).exists():
            return

        self._write(file_path, "")

    def read(self):
        """Reads the file config into memory."""
        with open(self.config_path, 'r') as file:
            # TODO: Finish load this into the instance.
            print(toml.loads(file.read()))

    def refresh(self):
        """Refreshes the memory config from the file."""
        ...

    def save(self):
        """Saves the current configuration to file."""
        config_content: str = toml.dumps(self.dict())
        self._write(self.config_path, config_content)
