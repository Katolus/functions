from typing import Any


class FunctionErrorMixin:
    code: str
    msg_template: str

    def __init__(self, **ctx: Any) -> None:
        self.__dict__ = ctx

    def __str__(self) -> str:
        return self.msg_template.format(**self.__dict__)

    # def __reduce__(self) -> Tuple[Callable[..., 'PydanticErrorMixin'], Tuple[Type['PydanticErrorMixin'], 'DictStrAny']]:
    #     return cls_kwargs, (self.__class__, self.__dict__)


class ValidatorMixin:
    # TODO: Update this to handle validation properly
    # Consider moving it back to the function error mixin since there is no value of this here
    @classmethod
    def __get_validators__(cls) -> "CallableGenerator":
        yield cls.validate

    @classmethod
    def validate(cls, value: Any) -> Any:
        
        return value
