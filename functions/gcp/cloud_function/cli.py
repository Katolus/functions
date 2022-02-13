"""Holds functions that interact with the gcloud cli tool"""
import functools
import itertools
import json
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import DirectoryPath
from pydantic import validate_arguments
from pydantic.types import Json

from functions import logs
from functions.config.managers import FunctionRegistry
from functions.config.models import FunctionRecord
from functions.constants import CloudStatus
from functions.constants import PROJECT_MARK
from functions.gcp.cloud_function.constants import CloudFunctionLabel
from functions.gcp.cloud_function.constants import Runtime
from functions.gcp.cloud_function.constants import TriggerType
from functions.gcp.constants import DEFAULT_GCP_REGION
from functions.gcp.constants import GCP_RESERVED_VARIABLES
from functions.processes import check_output
from functions.processes import run_cmd
from functions.types import DictStrAny

# Preinstalled dependencies
# https://cloud.google.com/functions/docs/writing/specifying-dependencies-python


@validate_arguments
def add_trigger_arguments(
    trigger_type: TriggerType, trigger_value: Optional[str] = None
) -> List[str]:
    """Returns a list of arguments to append that denote the type of trigger applied"""
    if trigger_value:
        return [trigger_type, trigger_value]
    else:
        return [trigger_type]


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


def add_update_labels_arguments(function: FunctionRecord) -> List[str]:
    """Adds labels to the scope of the deployment"""
    # https://cloud.google.com/sdk/gcloud/reference/functions/deploy#--update-labels

    function_labels: Dict[
        str, str
    ] = {}  # Temp until we can get the labels from the config
    default_labels = {
        CloudFunctionLabel.MARK: PROJECT_MARK,
        CloudFunctionLabel.NAME: function.name,
        # Consider adding versioning
    }
    # Zip function labels with default labels
    labels = {**default_labels, **(function_labels or {})}

    argument_template = "--update-labels={kv_pairs}"
    label_list = []
    for key, value in labels.items():
        label_list.append(f"{key}={value}")
    return [argument_template.format(kv_pairs=",".join(label_list))]


def add_region_argument(region: str = DEFAULT_GCP_REGION) -> List[str]:
    return ["--region", region]


def add_filter_argument(filter_labels: List[str] = None) -> List[str]:
    """Adds a filter argument to the gcloud command"""
    # https://cloud.google.com/sdk/gcloud/reference/functions/logs/read#--filter
    core_label = f"labels.{CloudFunctionLabel.MARK}:{PROJECT_MARK}"
    all_labels = " AND ".join([core_label] + (filter_labels or []))
    return [
        f"--filter='{all_labels}'",
    ]


@validate_arguments
def deploy_function(function: FunctionRecord, *, new_name: str = None):
    """Uses gcloud to deploy a cloud function"""
    cloud_function_name = new_name or function.name
    logs.debug(f"Deploying {cloud_function_name} as a cloud function")
    run_cmd(
        [
            "gcloud",
            "functions",
            "deploy",
            "--quiet",
            "--no-user-output-enabled",
            cloud_function_name,
        ]
        + add_runtime_arguments(function.config.deploy_variables.runtime)
        + add_source_arguments(Path(function.config.path))
        + add_entry_point_arguments(function.config.run_variables.entry_point)
        + add_ignore_file_arguments()
        + add_update_labels_arguments(function)
        + add_region_argument(function.config.deploy_variables.region)
        + add_env_vars_arguments(function.config.env_variables)
        + add_trigger_arguments(
            function.config.deploy_variables.trigger,
            function.config.deploy_variables.trigger_value,
        )
    )

    function.status.GCP = CloudStatus.DEPLOYED
    FunctionRegistry.update_function(function)
    logs.debug(f"Successfully deployed {cloud_function_name}")


def delete_function(function_name: str):
    """Runs a gcloud command to remove a function matching a given name"""
    logs.debug(f"Deleting cloud function: {function_name}")

    # Commands will error out if the function doesn't exist
    run_cmd(
        [
            "gcloud",
            "functions",
            "delete",
            "--quiet",
            "--no-user-output-enabled",
            function_name,
        ]
        + add_region_argument()
    )

    function = FunctionRegistry.fetch_function(function_name)
    function.status.GCP = CloudStatus.DELETED
    FunctionRegistry.update_function(function)

    logs.debug(f"Successfully deleted cloud function: {function_name}")


def run_describe_cmd(function: FunctionRecord) -> None:
    logs.debug(f"Reading cloud description of the function: {function.name}")
    run_cmd(["gcloud", "functions", "describe", function.name] + add_region_argument())


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
        + add_filter_argument()
    )


@functools.lru_cache
def fetch_functions_in_json() -> List[Json]:
    """Runs a gcloud command to list all functions"""
    logs.debug("Fetching cloud functions")
    # https://cloud.google.com/sdk/gcloud/reference/topic/formats#json
    cmd_result = check_output(["gcloud", "functions", "list", "--format", "json"])
    return json.loads(cmd_result)


@functools.lru_cache
def fetch_function_names() -> str:
    """Returns a list of cloud function names"""
    functions = fetch_functions_in_json()
    logs.debug(f"Fetched {len(functions)} cloud functions")
    return "Temp holder until I figure out how to get a function's name"


@functools.lru_cache
def fetch_deployed_function_names() -> List[str]:
    """Returns a list of cloud function names"""
    logs.debug("Fetching deployed cloud function names")
    cmd_result = check_output(
        [
            "gcloud",
            "functions",
            "list",
            "--format",
            f"get(labels.{CloudFunctionLabel.NAME.value})",
        ]
    )
    # Split the result into a list of strings
    return cmd_result.splitlines()
