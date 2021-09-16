import os
import subprocess
from typing import List

from pydantic import validate_arguments


@validate_arguments
def run_cmd(
    cmd_exec: List[str], capture_output: bool = False
) -> subprocess.CompletedProcess:
    # TODO: Add logging...
    return subprocess.run(cmd_exec, capture_output=capture_output)


@validate_arguments
def run_process(cmd_exec: List[str], **kwargs) -> subprocess.Popen:
    return subprocess.Popen(cmd_exec, **kwargs)


def run_locally(cwd=None, *, source: str, target: str, port: int) -> subprocess.Popen:
    process = subprocess.Popen(
        [
            "functions-framework",
            f"--source={source}",
            f"--target={target}",
            f"--port={port}",
        ],
        cwd=os.getcwd(),
        stdout=subprocess.PIPE,
    )
    return process


# Use pipe from one process to another
# p1 = run_process(["docker", "images", "-a"], stdout=subprocess.PIPE)
# p2 = run_process(["grep", "functions"], stdin=p1.stdout, stdout=subprocess.PIPE)
# functions: List[str] = p2.communicate()[0].decode("utf-8").strip().split("\n")
