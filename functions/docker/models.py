"""Set of typed models for managing docker processes and manipulation docker objects"""

from typing import Dict

from pydantic import BaseModel

from .enums import DockerLabel


class BuildArgs(BaseModel):
    TARGET: str
    SOURCE: str
    SIGNATURE_TYPE: str


class BuildVariables(BaseModel):
    path: str
    tag: str
    buildargs: BuildArgs
    labels: Dict[DockerLabel, str]
