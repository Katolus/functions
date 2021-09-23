import subprocess
from typing import Sequence

from pydantic import validate_arguments


@validate_arguments
def run_cmd(
    cmd_exec: Sequence[str], capture_output: bool = False
) -> subprocess.CompletedProcess:
    # TODO: Add logging...
    ...
    return subprocess.run(cmd_exec, capture_output=capture_output)


@validate_arguments
def run_process(cmd_exec: Sequence[str], **kwargs) -> subprocess.Popen:
    return subprocess.Popen(cmd_exec, **kwargs)
