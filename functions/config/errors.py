from functions.errors import FunctionBaseError


class ConfigValidationError(FunctionBaseError):
    code = "config.validation"
    msg_template = "Config file validation failed with error -> {error}"


class FunctionNotInRegistryError(FunctionBaseError):
    code = "config.function_not_in_registry"
    msg_template = "Function '{function}' not found in registry. Validate your setup."
