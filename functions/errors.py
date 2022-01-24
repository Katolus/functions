from typing import Any, Iterable, Optional

from click.exceptions import UsageError as ClickUsageError

from functions.types import ExceptionClass


class UsageError(ClickUsageError):
    """Wrapper class over click's error handler class"""

    pass


class FunctionBaseError(Exception):
    code: str
    msg_template: str
    original_error: Optional[ExceptionClass]

    def __init__(self, *, error: ExceptionClass = None, **kwargs: Any) -> None:
        self.original_error = error
        self.__dict__ = kwargs
        self.__dict__["error"] = str(error)
        super().__init__()

    def __str__(self) -> str:
        return (
            self.msg_template.format(**self.__dict__)
            if self.msg_template
            else "Unknown error occurred"
        )

    @property
    def message(self) -> str:
        return str(self)


class IsNotAValidDirectory(FunctionBaseError):
    code = "path.invalid_directory"
    msg_template = "Path '{path}' is not a valid function directory"


class ConfigNotFoundError(FunctionBaseError):
    code = "path.config_not_found"
    msg_template = "Path '{path}' does not include a valid config file"


class PathNotADirectoryError(FunctionBaseError):
    code = "path.not_a_directory"
    msg_template = 'Path "{path}" does not point to a directory'


class FunctionBuildError(FunctionBaseError):
    reason: str
    build_log: Iterable[str]  # For storing the build log in log files
    code = "functions.build_error"
    msg_template = "Function ({name}) build failed"

    def __init__(
        self,
        *,
        reason: str,
        build_log: Iterable[str],
        error: ExceptionClass = None,
        **kwargs: Any,
    ) -> None:
        self.reason = reason
        self.build_log = build_log
        super().__init__(error=error, **kwargs)


class FunctionNameTaken(FunctionBaseError):
    code = "functions.name_taken"
    msg_template = "Function with that name ('{name}') already exists"


class FunctionNotRunningError(FunctionBaseError):
    code = "functions.not_running"
    msg_template = "Function '{name}' is not running"


class FunctionNotFoundError(FunctionBaseError):
    code = "functions.not_found"
    msg_template = "Function '{name}' not found in registry. Try running `functions sync local` to synchronize built functions"


class FunctionImageNotFoundError(FunctionBaseError):
    code = "functions.image_not_found"
    msg_template = "Function's image ({image_id}) not found"


class FunctionContainerNotFoundError(FunctionBaseError):
    code = "functions.container_not_found"
    msg_template = "Function's container ({container_id}) not found"


class InvalidFunctionTypeError(FunctionBaseError):
    code = "functions.invalid_type"
    msg_template = "Function type ({type}) is not valid nor supported"


class ErrorRemovingResources(FunctionBaseError):
    code = "functions.error_removing_resources"
    msg_template = (
        "Cannot remove resources for function '{name}' -> {path}. Error: {error}"
    )
