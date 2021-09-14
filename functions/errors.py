from pydantic import PydanticValueError


class FunctionsError(Exception):
    ...



class ItIsNotAValidDirectory(PydanticValueError, FunctionsError):
    msg_template = "value is not a valid function directory"


class ConfigNotFoundError(PydanticValueError, FunctionsError):
    msg_template = "value does not include a valid config file"
