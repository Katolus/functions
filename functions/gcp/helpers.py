from functions.processes import check_if_cmd_exists


def check_if_gcloud_cmd_installed():
    """
    Check if gcloud command is installed
    """
    return check_if_cmd_exists(["gcloud", "--version"])
