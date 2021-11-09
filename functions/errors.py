from typing import Any, Generator, Optional

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
    build_log: Generator
    code = "functions.build_error"
    msg_template = "Function ({name}) build failed"

    def __init__(
        self,
        *,
        reason: str,
        build_log: Generator,
        error: ExceptionClass = None,
        **kwargs: Any,
    ) -> None:
        self.reason = reason
        self.build_log = build_log
        super().__init__(error=error, **kwargs)


class FunctionNameTaken(FunctionBaseError):
    code = "functions.name_taken"
    msg_template = "Function with that name ('{name}') already exists"


class InvalidFunctionTypeError(FunctionBaseError):
    code = "functions.invalid_type"
    msg_template = "Function type ({type}) is not valid nor supported"
