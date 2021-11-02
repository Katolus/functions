"""Holds functions that interact with the gcloud cli tool"""

import itertools
from typing import List, Optional

from pydantic import validate_arguments

from functions.config.models import FunctionConfig
from functions.processes import run_cmd
from functions.types import DictStrAny
from functions.types import NotEmptyStr
from functions.gcp.constants import GCP_RESERVED_VARIABLES
from functions.gcp.constants import DEFAULT_GCP_REGION


# Preinstalled dependencies
# https://cloud.google.com/functions/docs/writing/specifying-dependencies-python

# Example ENV variables
# {
#   "GCF_BLOCK_RUNTIME_go112": "410",
#   "FUNCTION_TARGET": "main",
#   "HOME": "/root",
#   "K_REVISION": "2",
#   "PYTHONUSERBASE": "/layers/google.python.pip/pip",
#   "PYTHONDONTWRITEBYTECODE": "1",
#   "DEBIAN_FRONTEND": "noninteractive",
#   "FUNCTION_SIGNATURE_TYPE": "http",
#   "PORT": "8080",
#   "GCF_BLOCK_RUNTIME_nodejs6": "410",
#   "PWD": "/workspace",
#   "GAE_RUNTIME": "python39",
#   "K_SERVICE": "test-funcion",
#   "PYTHONUNBUFFERED": "1",
#   "PATH": "/layers/google.python.pip/pip/bin:/opt/python3.9/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
#   "S2A_ACCESS_TOKEN": "e13755294ada4a6059f3cf3683a7b2f30b0052938e522063e640386830c6bdab",
#   "LD_LIBRARY_PATH": "/layers/google.python.pip/pip/lib",
#   "LC_CTYPE": "C.UTF-8",
#   "SERVER_SOFTWARE": "gunicorn/20.0.4",
# }

class GCPCloudFunction:
    @classmethod
    def add_trigger_arguments(cls) -> List[str]:
        """Returns a list of arguments to append that denote the type of trigger applied"""
        return ["--trigger-http"]

    @classmethod
    def add_runtime_arguments(cls) -> List[str]:
        """Returns runtime arguments"""
        return ["--runtime", "python39"]

    @classmethod
    def add_source_arguments(cls, function_dir: str) -> List[str]:
        """Returns source arguments"""
        return ["--source", str(function_dir)]


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
def add_entry_point_arguments(entry_point: NotEmptyStr) -> List[str]:
    """Adds entry point variables to the scope of the deployment"""
    return ["--entry-point", entry_point]


def add_ignore_file_arguments(files: Optional[List[str]] = None) -> List[str]:
    """Adds ignore file variables to the scope of the deployment"""
    default_ignores = ["config.json", "Dockerfile", ".dockerignore"]
    if not files:
        ingore_files = default_ignores
    else:
        ingore_files = files + default_ignores

    return list(
        itertools.chain.from_iterable(
            [["--ignore-file", filename] for filename in ingore_files]
        )
    )


def add_region_argument(region: Optional[str] = None) -> List[str]:
    # _region = region or app_config.config.default_region or GCP_REGION
    # app_config.config.default_region = _region
    # app_config.save()
    return ["--region", DEFAULT_GCP_REGION]


@validate_arguments
def deploy_function(config: FunctionConfig):
    """Uses gcloud to deploy a cloud function"""
    cloud_function_name = config.run_variables.name
    run_cmd(
        [
            "gcloud",
            "functions",
            "deploy",
            cloud_function_name,
        ]
        + GCPCloudFunction.add_runtime_arguments()
        + GCPCloudFunction.add_source_arguments(str(config.path))
        + add_entry_point_arguments(config.run_variables.entry_point)
        + add_ignore_file_arguments()
        + add_region_argument()
        + add_env_vars_arguments(config.env_variables)
        + GCPCloudFunction.add_trigger_arguments()
    )



def delete_function(function_name: str):
    """Runs a gcloud command to remove a function matching a given name"""
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
    run_cmd(["gcloud", "functions", "describe", function_name] + add_region_argument())


def read_logs(function_name: str):
    # The command below does not work as expected.
    run_cmd(
        [
            "gcloud",
            "functions",
            "logs",
            "read",
        ]
        + add_region_argument()
    )
