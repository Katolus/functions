"""Stores methods for autocompleting GCP commands"""

from typing import List


def names_of_functions_deployed_as_cloud_functions(gcp_project_id: str) -> List[str]:
    """Returns a list of names of functions deployed as cloud functions

    Args:
        gcp_project_id (str): The GCP project ID.

    Returns:
        list: A list of names of functions deployed as cloud functions.
    """
    from functions.gcp.cloud_functions import get_cloud_functions

    cloud_functions = get_cloud_functions(gcp_project_id)
    return [cloud_function.name for cloud_function in cloud_functions]
