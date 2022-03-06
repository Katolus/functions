import subprocess
from typing import Sequence

from pydantic import validate_arguments

from functions import logs


@validate_arguments
def run_cmd(
    cmd_exec: Sequence[str], capture_output: bool = False
) -> subprocess.CompletedProcess:
    """Runs a command"""
    logs.debug(f"Running command: {cmd_exec}")
    return subprocess.run(cmd_exec, capture_output=capture_output, check=True)


@validate_arguments
def run_process(cmd_exec: Sequence[str], **kwargs) -> subprocess.Popen:
    """Runs a process"""
    logs.debug(f"Running process: {cmd_exec}")
    return subprocess.Popen(cmd_exec, **kwargs)


@validate_arguments
def check_output(cmd_exec: Sequence[str]) -> str:
    """Runs a process and returns the output"""
    logs.debug(f"Running command: {cmd_exec}")
    return subprocess.check_output(cmd_exec, stderr=subprocess.STDOUT).decode()


@validate_arguments
def check_if_cmd_exists(cmd_exec: Sequence[str]) -> bool:
    """Checks if a command exists"""
    try:
        run_cmd(cmd_exec, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False
