from typing import Optional

from functions.docker.enums import DockerLabel


# TODO: Update types and more robust definition
def get_function_name_from_labels(labels: dict) -> Optional[str]:
    """Returns a function name from docker labels"""
    return labels.get(DockerLabel.FUNCTION_NAME)
