from pydantic import BaseModel
from pydantic.dataclasses import dataclass


@dataclass
class DockerImage:
    id: str
    repository: str
    tag: str
    created: str
    size: str


# Config
class RunVariables(BaseModel):
    entry_point: str
    name: str
    port: int
    signature_type: str
    source: str


class EnvVariables(BaseModel):
    pass


class DeployVariables(BaseModel):
    provider: str
    service: str


class Config(BaseModel):
    run_variables: RunVariables
    env_variables: EnvVariables
    deploy_variables: DeployVariables
