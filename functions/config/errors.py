from functions.errors import FunctionBaseError


class ConfigValidationError(FunctionBaseError):
    code = "config.validation"
    msg_template = "Config file validation failed with error -> {error}"
