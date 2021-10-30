def get_cloud_functions(project_id: str, region: str):
    """
    Get all cloud functions in a project and region.
    """
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from oauth2client.client import GoogleCredentials

    credentials = GoogleCredentials.get_application_default()
    service = build("cloudfunctions", "v1", credentials=credentials)

    request = (
        service.projects()
        .locations()
        .functions()
        .list(parent="projects/{}/locations/{}".format(project_id, region))
    )

    try:
        response = request.execute()
        return response
    except HttpError as e:
        print("Error: {}".format(e))
        return None
