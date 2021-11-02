import google.auth  # type: ignore
from googleapiclient.discovery import build  # type: ignore
from googleapiclient.errors import HttpError  # type: ignore

from ..constants import DEFAULT_GCP_REGION
from .errors import DeploymentError

# TODO: Test out the functionality on machines with a default login
# TODO: Handle DefaultCredentialsError
credentials, default_project_id = google.auth.default()


def deploy(
    function_name: str,
    *,
    entry_point: str,
    runtime: str,
    source_path: str,
    trigger: dict = None,  # TODO: Add a specific type for triggers
    region: str = DEFAULT_GCP_REGION,
    project_id: str = default_project_id,
):
    """
    Deploy a cloud function to a project and region.
    """

    service = build("cloudfunctions", "v1", credentials=credentials)

    body = {
        "name": function_name,
        "sourceArchiveUrl": source_path,
        "entryPoint": entry_point,
        "runtime": runtime,
        "httpsTrigger": {},
    }
    if trigger:
        body["httpsTrigger"] = trigger

    request = (
        service.projects()
        .locations()
        .functions()
        .create(
            parent=f"projects/{project_id}/locations/{region}",
            body=body,
        )
    )

    try:
        response = request.execute()
        return response
    except HttpError as e:
        raise DeploymentError(error=e)
