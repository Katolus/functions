from functions.errors import FunctionBaseError


class UnknownServiceError(FunctionBaseError):
    code = "gcp.unknown_service"
    msg_template = "Unknown GCP service: {service}"
