from __future__ import annotations

from enum import Enum


class AppConfigVersion(str, Enum):
    """A set of version constants for app config files"""

    V1: str = "2022-02-04"

    @classmethod
    def latest(cls) -> AppConfigVersion:
        """
        Returns the latest version of the config.
        """
        return max(cls, key=lambda version: version.value)


class FunctionConfigVersion(str, Enum):
    """A set of version constants for function config files"""

    V1: str = "2022-02-04"

    @classmethod
    def latest(cls) -> FunctionConfigVersion:
        """
        Returns the latest version of the config.
        """
        return max(cls, key=lambda version: version.value)
