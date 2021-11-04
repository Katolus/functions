from typing import NoReturn

import typer

from functions import logs
from functions import user
from functions.error_handlers import error_handler

from .errors import ConfigValidationError


@error_handler(error=ConfigValidationError)
def handle_config_validation_error(error: ConfigValidationError) -> NoReturn:
    logs.exception(error.original_error)
    user.fail(error.message)
    raise typer.Exit()
