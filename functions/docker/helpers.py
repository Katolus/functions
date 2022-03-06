from typing import Optional

from functions.docker.enums import DockerLabel
from functions.docker.types import DockerLabelsDict


def get_function_name_from_labels(labels: DockerLabelsDict) -> Optional[str]:
    """Returns a function name from docker labels"""
    return labels.get(DockerLabel.FUNCTION_NAME)
