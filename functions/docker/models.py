import json
import re
from typing import Dict, List

import docker
from docker.utils import build
from docker.utils.json_stream import json_stream
from pydantic import BaseModel

from functions import logs
from functions.config.models import FunctionRecord
from functions.docker.types import DockerBuildAPIGenerator
from functions.errors import FunctionBuildError

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


class DockerManager(BaseModel):
    """
    Manages all the docker processses
    """

    client: docker.client.DockerClient

    def __init__(self) -> None:
        self.client = docker.from_env()

    def _construct_build_variables(self, function: FunctionRecord) -> BuildVariables:
        """
        Constructs the build variables for the docker build process from a function
        """
        logs.debug(f"Constructing build variables for {function.name}")
        config = function.config
        return BuildVariables.parse_obj(
            {
                {
                    "path": config.path,
                    "tag": function.name,
                    "buildargs": {
                        "TARGET": config.run_variables.entry_point,
                        "SOURCE": config.run_variables.source,
                        "SIGNATURE_TYPE": config.run_variables.signature_type,
                    },
                    "labels": {
                        DockerLabel.FUNCTION_NAME: function.name,
                        DockerLabel.FUNCTION_PATH: config.path,
                        DockerLabel.CONFIG_PATH: config.config_path,
                        DockerLabel.CONFIG: json.dumps(config.json()),
                        DockerLabel.ORGANISATION: "Ventress",
                    },
                }
            }
        )

    def _call_build_api(self, function: FunctionRecord) -> DockerBuildAPIGenerator:
        """
        Calls docker's build API and serves the output

        This function is not ideally asynchronous back to the console.
        Most likely due to to fact the request to the API does not release
        unless it makes an external call. Not sure, but I really don't want to
        spend more time making this work. Not benefit.
        """
        build_variables = self._construct_build_variables(function)

        # Snippet copied and adjusted from the docker-py
        # package to account for stream logs as build takes place.
        resp = self.client.api.build(**build_variables.dict())
        result_stream = json_stream(resp)

        last_event = None
        image_id = None

        for chunk in result_stream:
            if "error" in chunk:
                raise FunctionBuildError(
                    name=function.name, reason=chunk["error"], build_log=result_stream
                )
            if "stream" in chunk:
                match = re.search(
                    r"(^Successfully built |sha256:)([0-9a-f]+)$", chunk["stream"]
                )
                if match:
                    image_id = match.group(2)
            last_event = chunk
            yield image_id, last_event.get("stream")

    def build_image(self, function: FunctionRecord, show_logs: bool) -> DockerImage:
        """
        Builds the image for the function
        """
        logs.debug(f"Building image for {function.name}")

        image_id, logs = self._call_build_api(function)
        if show_logs:
            print(logs)
        return DockerImage(image_id)

    def get_containers(self) -> List:
        """
        Returns a list of all the containers
        """
        return self.client.containers.list()

    def get_container(self, name: str):
        """
        Returns a container by name
        """
        return self.client.containers.get(name)
