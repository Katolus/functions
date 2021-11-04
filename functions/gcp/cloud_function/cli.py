"""Holds functions that interact with the gcloud cli tool"""
import functools
import itertools
import json
from pathlib import Path
from typing import List, Optional

from pydantic import DirectoryPath
from pydantic import validate_arguments
from pydantic.types import Json

from functions import logs
from functions.config.managers import FunctionRegistry
from functions.config.models import FunctionConfig
from functions.config.models import FunctionRecord
from functions.constants import FunctionStatus
from functions.gcp.cloud_function.constants import Runtime
from functions.gcp.cloud_function.constants import Trigger
from functions.gcp.constants import DEFAULT_GCP_REGION
from functions.gcp.constants import GCP_RESERVED_VARIABLES
from functions.processes import check_output
from functions.processes import run_cmd
from functions.types import DictStrAny

# Preinstalled dependencies
# https://cloud.google.com/functions/docs/writing/specifying-dependencies-python


@validate_arguments
def add_trigger_arguments(trigger: Trigger) -> List[str]:
    """Returns a list of arguments to append that denote the type of trigger applied"""
    return [trigger]


@validate_arguments
def add_runtime_arguments(runtime: Runtime) -> List[str]:
    """Returns runtime arguments"""
    return ["--runtime", runtime]


@validate_arguments
def add_source_arguments(function_dir: DirectoryPath) -> List[str]:
    """Returns source arguments"""
    return ["--source", str(function_dir)]


@validate_arguments
def add_env_vars_arguments(env_variables: DictStrAny) -> List[str]:
    """Adds environmental variables to the scope of the deployment if any are present"""
    # https://cloud.google.com/sdk/gcloud/reference/functions/deploy#--set-env-vars
    env_list = []
    for key, value in env_variables.items():
        if not value:
            continue

        if variable := GCP_RESERVED_VARIABLES.get(key):
            raise ValueError(
                f"ENV variable '{key}' cannot be set -> {variable['description']}"
            )
        env_list.append(["--set-env-vars", f"{key}={value}"])
    return list(itertools.chain.from_iterable(env_list))


@validate_arguments
def add_entry_point_arguments(entry_point: str) -> List[str]:
    """Adds entry point variables to the scope of the deployment"""
    return ["--entry-point", entry_point]


def add_ignore_file_arguments(files: Optional[List[str]] = None) -> List[str]:
    """Adds ignore file variables to the scope of the deployment"""
    default_ignores = ["config.json", "Dockerfile", ".dockerignore"]

    # Combine default files and files
    ingore_files = default_ignores + (files or [])

    return list(
        itertools.chain.from_iterable(
            [["--ignore-file", filename] for filename in ingore_files]
        )
    )


def add_update_labels_arguments(labels: DictStrAny) -> List[str]:
    """Adds labels to the scope of the deployment"""
    # https://cloud.google.com/sdk/gcloud/reference/functions/deploy#--update-labels
    label_list = []
    for key, value in labels.items():
        label_list.append(["--set-labels", f"{key}={value}"])
    return list(itertools.chain.from_iterable(label_list))


def add_region_argument(region: str = DEFAULT_GCP_REGION) -> List[str]:
    return ["--region", region]


@validate_arguments
def deploy_function(cloud_function_name: str, config: FunctionConfig):
    """Uses gcloud to deploy a cloud function"""
    logs.debug(f"Deploying cloud function: {cloud_function_name}")
    run_cmd(
        [
            "gcloud",
            "functions",
            "deploy",
            cloud_function_name,
        ]
        + add_runtime_arguments(config.deploy_variables.runtime)
        + add_source_arguments(Path(config.path))
        + add_entry_point_arguments(config.run_variables.entry_point)
        + add_ignore_file_arguments()
        + add_region_argument(config.deploy_variables.region)
        + add_env_vars_arguments(config.env_variables)
        + add_trigger_arguments(config.deploy_variables.trigger)
    )
    FunctionRegistry.update_function(
        FunctionRecord(
            name=cloud_function_name, config=config, status=FunctionStatus.DEPLOYED
        )
    )


def delete_function(function_name: str):
    """Runs a gcloud command to remove a function matching a given name"""
    logs.debug(f"Deleting cloud function: {function_name}")
    run_cmd(
        [
            "gcloud",
            "functions",
            "delete",
            function_name,
        ]
        + add_region_argument()
    )


def describe_function(function_name: str):
    logs.debug(f"Reading cloud description of the function: {function_name}")
    run_cmd(["gcloud", "functions", "describe", function_name] + add_region_argument())


def fetch_function_logs(function: FunctionRecord):
    logs.debug(f"Reading logs for {function.name}")
    run_cmd(
        [
            "gcloud",
            "functions",
            "logs",
            "read",
        ]
        + add_region_argument(function.config.deploy_variables.region)
    )


@functools.cache
def fetch_functions() -> List[Json]:
    """Runs a gcloud command to list all functions"""
    logs.debug("Fetching cloud functions")
    cmd_result = check_output(["gcloud", "functions", "list", "--format", "json"])
    return json.loads(cmd_result)


@functools.cache
def fetch_function_names() -> str:
    """Returns a list of cloud function names"""
    functions = fetch_functions()
    logs.debug(f"Fetched {len(functions)} cloud functions")
    return "Temp holder until I figure out how to get a function's name"
