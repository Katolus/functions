from functions.errors import FunctionBaseError


class ComponentMissingError(FunctionBaseError):
    code = "docker.missing_engine_error"
    msg_template = (
        "It looks like the `{component}` is not missing or not installed correctly."
    )


class ComponentVersionError(FunctionBaseError):
    code = "docker.engine_version_error"
    msg_template = "It looks like `{component}'s` version is too old ({version}). Please update to - {min_version} minimum."
