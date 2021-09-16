from pathlib import Path

from pydantic import PydanticValueError


class FunctionsError(Exception):
    ...


class _PathValueError(PydanticValueError):
    def __init__(self, *, path: Path) -> None:
        super().__init__(path=str(path))


class ItIsNotAValidDirectory(_PathValueError, FunctionsError):
    code = "path.invalid_directory"
    msg_template = "path '{path}' is not a valid function directory"


class ConfigNotFoundError(_PathValueError, FunctionsError):
    code = "code.config_not_found"
    msg_template = "path '{path}' does not include a valid config file"
