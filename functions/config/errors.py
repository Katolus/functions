from functions.errors import FunctionBaseError


class ConfigValidationError(FunctionBaseError):
    code = "config.validation"
    msg_template = "Config file validation failed with error -> {error}"


class FunctionNotInRegistryError(FunctionBaseError):
    code = "config.function_not_in_registry"
    msg_template = "Function '{function}' not found in registry. Validate your setup."


class AppConfigVersionError(FunctionBaseError):
    code = "config.app_config_version_missmatch"
    msg_template = (
        "Incompatible version of the configuration file: {current_version} vs {version}"
    )
