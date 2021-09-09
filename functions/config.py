import json
import fnmatch
import os
from typing import Optional, Union

from pydantic import DirectoryPath
from pydantic import FilePath
from pydantic import validate_arguments

from functions.hints import Config


@validate_arguments
def load_config(config_path: FilePath) -> Config:
    """Load a configuration file into a Python object."""
    config = None
    with open(config_path, "r") as file:
        config = json.load(file)

    return Config(**config)


def get_config_path(dir_path: Union[os.DirEntry, DirectoryPath]) -> Optional[str]:
    """Returns a config path if present."""
    for filename in os.listdir(dir_path):
        if fnmatch.fnmatch(filename, "config.json"):
            return os.path.join(dir_path, filename)
    return None
