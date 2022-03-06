import functools

from functions.processes import check_if_cmd_exists
from functions.processes import run_cmd


@functools.cache
def check_if_gcloud_cmd_installed() -> bool:
    """Check if gcloud command is installed"""

    return check_if_cmd_exists(["gcloud", "--version"])


@functools.cache
def current_project() -> str:
    """Returns current working project"""

    output = run_cmd(["gcloud", "config", "get-value", "project"])
    return output.stdout.strip()
