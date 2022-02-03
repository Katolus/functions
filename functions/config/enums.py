from __future__ import annotations

from enum import Enum


class AppConfigVersion(str, Enum):
    """A set of version constants"""

    V1: str = "2022-02-04"

    @classmethod
    def latest(cls) -> AppConfigVersion:
        """
        Returns the latest version of the config.
        """
        return max(cls, key=lambda version: version.value)
