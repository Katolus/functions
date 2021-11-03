from functions.errors import FunctionBaseError


class UnknownServiceError(FunctionBaseError):
    code = "gcp.unknown_service"
    msg_template = "Unknown GCP service: {service}"

    def __init__(self, *, service: str) -> None:
        super().__init__(service=service)
